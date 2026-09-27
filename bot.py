# PROD_LAUNCHER: Bridge to run engine.py and satisfy Render's startup profile
import subprocess
import sys

if __name__ == '__main__':
    print("🚀 Launcher Bridge Activated: Booting up engine.py on Render...")
    # Natively hands over execution straight to your advanced engine.py code
    result = subprocess.run([sys.executable, "engine.py"])
    sys.exit(result.returncode)

