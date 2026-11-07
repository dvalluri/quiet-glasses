"""Exercise hardware failure contracts that the emulator normally masks.

These are app-level fault injections, not physical-device validation or SDK edits.
"""
from pathlib import Path
import time
from halo_emulator import HaloEmulator

DEVICE = Path(__file__).resolve().parents[1] / 'quiet_glasses' / 'device'

def wait_for(emu, condition):
    deadline = time.monotonic() + 2
    while not condition():
        assert emu.get_error() is None, str(emu.get_error())
        assert time.monotonic() < deadline
        time.sleep(.005)

def test_panel_wakes_before_text(tmp_path):
    emu = HaloEmulator(sandbox_dir=tmp_path, print_handler=None)
    emu.load_directory(str(DEVICE))
    (tmp_path / 'contract.lua').write_text('''
        frame.display.power_save(true)
        local text = frame.display.text
        frame.display.text = function(...)
            assert(not frame.display.power_save(), 'physical panel is suspended')
            text(...)
        end
        require('main')
    ''')
    try:
        emu.start('contract.lua')
        wait_for(emu, lambda: b'READY' in emu.get_bluetooth_sent())
        emu.inject_bluetooth_data(b'A|1')
        emu.inject_bluetooth_data(b'T|1|1|Hello Halo')
        wait_for(emu, lambda: b'DRAWN|1|1' in emu.get_bluetooth_sent())
        assert emu.get_framebuffer().convert('RGB').getbbox()
    finally:
        emu.stop()

def test_offline_boot_and_button_clear_survive_send_failure(tmp_path):
    emu = HaloEmulator(sandbox_dir=tmp_path, print_handler=None)
    emu.load_directory(str(DEVICE))
    (tmp_path / 'contract.lua').write_text('''
        frame.bluetooth.send = function() error('not connected') end
        require('main')
    ''')
    try:
        emu.start('contract.lua')
        time.sleep(.04)
        assert emu.is_running()
        assert emu.get_error() is None
        emu.inject_bluetooth_data(b'A|1')
        emu.inject_bluetooth_data(b'T|1|1|Hello Halo')
        wait_for(emu, lambda: emu.get_framebuffer().convert('RGB').getbbox())
        emu.inject_button_single()
        wait_for(emu, lambda: not emu.get_framebuffer().convert('RGB').getbbox())
        assert emu.is_running()
    finally:
        emu.stop()
