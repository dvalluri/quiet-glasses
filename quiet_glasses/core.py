import asyncio
import time
import textwrap
import unicodedata
from pathlib import Path
from halo_emulator import HaloEmulator


def layout(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    text = ''.join(c if 32 <= ord(c) <= 126 else ' ' for c in text)
    text = ' '.join(text.split())
    lines = textwrap.wrap(text, width=28, break_long_words=True, break_on_hyphens=False)
    return '\n'.join(lines[-6:])


class EmulatorTransport:
    def __init__(self, sandbox):
        self.emulator = HaloEmulator(sandbox_dir=sandbox, print_handler=None)
        self.cursor = 0

    def start(self):
        self.emulator.load_directory(str(Path(__file__).parent / 'device'))
        self.emulator.start('main.lua')

    def send(self, data):
        if len(data) > 240: raise ValueError('packet too large')
        self.emulator.inject_bluetooth_data(data)

    def receive(self):
        if self.emulator.get_error(): raise RuntimeError('Lua runtime failed')
        messages = self.emulator.get_bluetooth_sent()
        new = messages[self.cursor:]
        self.cursor = len(messages)
        return [m.decode('ascii') for m in new]

    def close(self):
        self.emulator.stop()


class HUD:
    def __init__(self, transport, provider):
        self.transport, self.provider = transport, provider
        self.generation = 0
        self.task = None
        self.acks = set()
        self.metrics = {}  # timings only; no prompt or response logging
        self.reader = None

    async def start(self):
        self.transport.start()
        self.reader = asyncio.create_task(self._read())
        await self._ack('READY')

    async def _read(self):
        while True:
            for message in self.transport.receive():
                self.acks.add(message)
                if message.startswith('DISMISSED|'):
                    if int(message.split('|')[1]) == self.generation:
                        self._cancel()
            await asyncio.sleep(0.001)

    async def _ack(self, message):
        async with asyncio.timeout(1):
            while message not in self.acks:
                if self.reader.done(): self.reader.result()
                await asyncio.sleep(0.001)
        self.acks.remove(message)

    def _cancel(self):
        if self.task and not self.task.done(): self.task.cancel()

    async def activate(self, prompt):
        if not prompt.strip(): raise ValueError('Prompt must not be empty')
        activated_at = time.perf_counter()
        await self.dismiss()
        self.generation += 1
        g = self.generation
        self.metrics = {'activated_at': activated_at}
        self.transport.send(f'A|{g}'.encode())
        await self._ack(f'ACTIVE|{g}')
        self.task = asyncio.create_task(self._stream(g, prompt))
        return self.task

    async def _stream(self, g, prompt):
        text, previous, seq = '', '', 0
        last_draw = 0.0
        try:
            async with asyncio.timeout(60):
                async for token in self.provider.stream(prompt):
                    if g != self.generation: return
                    self.metrics.setdefault('first_provider_ms',
                        (time.perf_counter() - self.metrics['activated_at']) * 1000)
                    text = (text + token)[-4096:]
                    shown = layout(text)
                    if not shown or shown == previous: continue
                    # First text draws immediately; later redraws are capped at 30 Hz.
                    if seq:
                        await asyncio.sleep(max(0, 1 / 30 - (time.perf_counter() - last_draw)))
                    seq += 1
                    self.transport.send(f'T|{g}|{seq}|{shown}'.encode('ascii'))
                    await self._ack(f'DRAWN|{g}|{seq}')
                    last_draw = time.perf_counter()
                    self.metrics.setdefault('first_display_ms',
                        (time.perf_counter() - self.metrics['activated_at']) * 1000)
                    previous = shown
        except asyncio.CancelledError:
            raise
        except Exception:
            self.metrics['failed'] = True
            self.transport.send(f'D|{g}'.encode())
            raise

    async def dismiss(self):
        self._cancel()
        # Queue clear before waiting for provider cleanup.
        dismissed = f'DISMISSED|{self.generation}'
        self.acks.discard(dismissed)
        self.transport.send(f'D|{self.generation}'.encode())
        if self.task:
            await asyncio.gather(self.task, return_exceptions=True)
        if self.reader and not self.reader.done():
            await self._ack(dismissed)
        self.acks.clear()

    async def close(self):
        try:
            await self.dismiss()
        finally:
            if self.reader:
                self.reader.cancel()
                await asyncio.gather(self.reader, return_exceptions=True)
            self.transport.close()
