# PROD_LAUNCHER: Bridge to run engine.py with unbuffered logs enabled
import subprocess
import sys

if __name__ == '__main__':
    print("🚀 Launcher Bridge Activated: Booting up engine.py with UNBUFFERED logging...")
    
    # FIXED: Added the '-u' flag to force Python to flush thread logs straight to Render dashboard console live
    result = subprocess.run([sys.executable, "-u", "engine.py"])
    sys.exit(result.returncode)
