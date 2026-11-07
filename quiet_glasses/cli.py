import argparse
import asyncio
import json
import tempfile
import sys
import os
import time
from .core import HUD, EmulatorTransport
from .providers import choose_provider

async def window(hud):
    import pygame
    pygame.display.init()
    screen = pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Quiet Glasses — Space dismisses')
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    await hud.dismiss()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    hud.transport.emulator.inject_button_single()
            image = hud.transport.emulator.get_framebuffer()
            surface = pygame.image.fromstring(image.tobytes(), image.size, 'RGBA')
            screen.blit(pygame.transform.scale(surface, (512, 512)), (0, 0))
            pygame.display.flip()
            if hud.metrics and 'first_visible_ms' not in hud.metrics:
                if image.convert('RGB').getbbox():
                    hud.metrics['first_visible_ms'] = (time.perf_counter() - hud.metrics['activated_at']) * 1000
                    print(f"\nFirst visible window frame: {hud.metrics['first_visible_ms']:.1f} ms", flush=True)
            await asyncio.sleep(1 / 30)
    finally:
        pygame.display.quit()

async def run(args):
    provider, description = await choose_provider(args.provider, args.endpoint, args.model)
    print('Provider:', description, flush=True)
    with tempfile.TemporaryDirectory(prefix='quiet-glasses-') as sandbox:
        hud = HUD(EmulatorTransport(sandbox), provider)
        viewer = None
        console = None
        try:
            await hud.start()
            if args.window: viewer = asyncio.create_task(window(hud))
            print('Blank HUD. /ask PROMPT activates; /dismiss clears; /save PATH captures; /quit exits.')
            reader = asyncio.StreamReader()
            console, _ = await asyncio.get_running_loop().connect_read_pipe(
                lambda: asyncio.StreamReaderProtocol(reader), sys.stdin)
            while True:
                print('> ', end='', flush=True)
                raw = await reader.readline()
                if not raw: break
                line = raw.decode('utf-8', errors='replace').rstrip('\r\n')
                if line == '/quit': break
                if line == '/dismiss': await hud.dismiss()
                elif line.startswith('/ask '):
                    task = await hud.activate(line[5:])
                    def completed(task):
                        if not task.cancelled():
                            error = task.exception()
                            print('Provider failed; HUD cleared. Use --provider mock for the mock fallback.' if error else json.dumps(hud.metrics), flush=True)
                    task.add_done_callback(completed)
                elif line.startswith('/save '):
                    hud.transport.emulator.get_framebuffer().save(line[6:])
        except (EOFError, KeyboardInterrupt):
            pass
        finally:
            if console: console.close()
            if viewer:
                viewer.cancel()
                await asyncio.gather(viewer, return_exceptions=True)
            await hud.close()

def main():
    parser = argparse.ArgumentParser(description='Quiet Glasses emulator host')
    parser.add_argument('--window', action='store_true', help='Show the emulator framebuffer')
    parser.add_argument('--provider', choices=['auto', 'mock', 'local'], default='auto')
    parser.add_argument('--endpoint', default=os.environ.get('QUIET_GLASSES_ENDPOINT', 'http://127.0.0.1:11434/v1/chat/completions'))
    parser.add_argument('--model', default=os.environ.get('QUIET_GLASSES_MODEL', 'gpt-oss:20b'))
    asyncio.run(run(parser.parse_args()))

if __name__ == '__main__': main()
