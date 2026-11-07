import subprocess
import sys

def test_cli_quits_cleanly():
    result = subprocess.run([sys.executable, '-m', 'quiet_glasses.cli', '--provider', 'mock'],
        input='/quit\n', capture_output=True, text=True, timeout=5)
    assert result.returncode == 0, result.stderr
    assert 'Blank HUD' in result.stdout
