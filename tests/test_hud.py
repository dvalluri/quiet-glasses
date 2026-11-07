import asyncio
import pytest
from quiet_glasses.core import HUD, EmulatorTransport, layout
from quiet_glasses.providers import MockProvider, LocalProvider

async def until(predicate):
    async with asyncio.timeout(2):
        while not predicate(): await asyncio.sleep(.005)

def bright(hud):
    return any(r or g or b for r, g, b, a in hud.transport.emulator.get_framebuffer().getdata())

@pytest.fixture
async def hud(tmp_path):
    app = HUD(EmulatorTransport(tmp_path), MockProvider(delay=.005))
    await app.start()
    yield app
    await app.close()

async def test_blank_stream_and_metric(hud):
    assert not bright(hud)
    task = await hud.activate('hello')
    await task
    assert bright(hud)
    assert 0 < hud.metrics['first_display_ms'] < 1000
    await hud.dismiss()
    await until(lambda: not bright(hud))

async def test_button_dismiss_prevents_late_packets(hud):
    hud.provider = MockProvider(text='word ' * 1000, delay=.005)
    task = await hud.activate('hello')
    await until(lambda: bright(hud))
    g = hud.generation
    hud.transport.emulator.inject_button_single()
    await until(lambda: not bright(hud))
    await until(task.done)
    hud.transport.send(f'T|{g}|999|LATE'.encode())
    await asyncio.sleep(.03)
    assert not bright(hud)
    assert task.cancelled()

async def test_reactivation_and_stale_generations(hud):
    first = await hud.activate('one')
    second = await hud.activate('two')
    await second
    assert first.done()
    await hud.dismiss()
    hud.transport.send(b'A|1')
    hud.transport.send(b'T|1|999|STALE')
    await asyncio.sleep(.03)
    assert not bright(hud)

async def test_provider_failure_clears(hud):
    class Broken:
        async def stream(self, prompt):
            yield 'Hello'
            raise RuntimeError('private content')
    hud.provider = Broken()
    task = await hud.activate('secret')
    with pytest.raises(RuntimeError): await task
    await until(lambda: not bright(hud))
    assert hud.metrics['failed']
    assert 'secret' not in str(hud.metrics)

async def test_host_dismiss_cancels_waiting_provider(hud):
    hud.provider = MockProvider(delay=30)
    task = await hud.activate('hello')
    await asyncio.wait_for(hud.dismiss(), .2)
    assert task.cancelled()
    await until(lambda: not bright(hud))

def test_layout():
    result = layout('café\x00 ' + 'longword' * 200)
    assert len(result.splitlines()) <= 6
    assert all(len(line) <= 28 for line in result.splitlines())
    assert result.isascii()

@pytest.mark.parametrize('url', ['https://example.com', 'http://192.168.1.2:8080',
    'http://localhost:8080', 'http://user:pass@127.0.0.1:8080'])
def test_local_only(url):
    with pytest.raises(ValueError): LocalProvider(url)

async def test_device_rejects_old_sequence_and_malformed(hud):
    task = await hud.activate('hello')
    await task
    image = hud.transport.emulator.get_framebuffer().tobytes()
    g = hud.generation
    for packet in [b'invalid', f'T|{g}|0|OLD'.encode(), f'T|{g}|x|BAD'.encode(), b'D|0']:
        hud.transport.send(packet)
    await asyncio.sleep(.03)
    assert hud.transport.emulator.get_framebuffer().tobytes() == image

async def test_missing_draw_ack_times_out_and_clears(hud):
    original = hud.transport.receive
    hud.transport.receive = lambda: [m for m in original() if not m.startswith('DRAWN|')]
    task = await hud.activate('hello')
    with pytest.raises(TimeoutError): await task
    await until(lambda: not bright(hud))
    assert 'first_display_ms' not in hud.metrics

async def test_window_renders_and_dismisses(hud, monkeypatch):
    monkeypatch.setenv('SDL_VIDEODRIVER', 'dummy')
    from quiet_glasses.cli import window
    import pygame
    task = await hud.activate('hello')
    await task
    viewer = asyncio.create_task(window(hud))
    try:
        await until(pygame.display.get_init)
        await until(lambda: 'first_visible_ms' in hud.metrics)
        assert hud.metrics['first_visible_ms'] > 0
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        await until(lambda: not bright(hud))
    finally:
        viewer.cancel()
        await asyncio.gather(viewer, return_exceptions=True)
