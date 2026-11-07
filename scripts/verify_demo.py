"""Reproduce the real-provider demo and save only its deliberately public output."""
import asyncio
import json
from pathlib import Path
import tempfile
import time
import pygame
from quiet_glasses.cli import window
from quiet_glasses.core import HUD, EmulatorTransport
from quiet_glasses.providers import LocalProvider

async def wait_for(predicate):
    async with asyncio.timeout(60):
        while not predicate(): await asyncio.sleep(.002)

async def main():
    artifacts = Path('artifacts/real-demo')
    artifacts.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as sandbox:
        hud = HUD(EmulatorTransport(sandbox), LocalProvider(
            'http://127.0.0.1:11434/v1/chat/completions', 'gpt-oss:20b'))
        viewer = None
        try:
            await hud.start()
            viewer = asyncio.create_task(window(hud))
            await wait_for(pygame.display.get_init)
            await asyncio.sleep(.05)
            pygame.image.save(pygame.display.get_surface(), str(artifacts / '01-blank.png'))
            question = 'In two short sentences, why does the sky look blue?'
            task = await hud.activate(question)
            await wait_for(lambda: 'first_visible_ms' in hud.metrics or task.done())
            if task.done(): await task
            pygame.image.save(pygame.display.get_surface(), str(artifacts / '02-first-visible.png'))
            await task
            await asyncio.sleep(.05)
            pygame.image.save(pygame.display.get_surface(), str(artifacts / '03-answer.png'))
            drawn = [m for m in hud.transport.emulator.get_bluetooth_sent() if m.startswith(b'DRAWN|')]
            start = time.perf_counter()
            hud.transport.emulator.inject_button_single()
            await wait_for(lambda: not hud.transport.emulator.get_framebuffer().convert('RGB').getbbox())
            clear_ms = (time.perf_counter() - start) * 1000
            await asyncio.sleep(.05)
            pygame.image.save(pygame.display.get_surface(), str(artifacts / '04-dismissed.png'))
            report = {'provider': 'Ollama gpt-oss:20b', 'question': question,
                      'metrics': hud.metrics.copy(), 'drawn_snapshots': len(drawn),
                      'button_to_blank_framebuffer_ms': clear_ms,
                      'display_driver': pygame.display.get_driver(),
                      'blank_after_dismissal': not hud.transport.emulator.get_framebuffer().convert('RGB').getbbox()}
            (artifacts / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
            print(json.dumps(report, indent=2), flush=True)
        finally:
            if viewer:
                viewer.cancel()
                await asyncio.gather(viewer, return_exceptions=True)
            await hud.close()

asyncio.run(main())
