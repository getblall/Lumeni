import os
import sys
import subprocess

# Dynamically force-install missing core dependencies inside the runner environment
try:
    import requests
except ImportError:
    print("Core dependency 'requests' missing. Installing automatically...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

try:
    import sympy as sp
except ImportError:
    print("Core dependency 'sympy' missing. Installing automatically...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sympy"])
    import sympy as sp

import base64
import time
import threading

# Dynamically handle Flask (Only required on Render, completely optional for GitHub Actions)
try:
    from flask import Flask
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    print("Flask module not detected. Proceeding in headless compiler mode...")

# Initialize Flask only if it is available
if HAS_FLASK:
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Lumeni Engine is fully operational and syncing on autopilot.", 200

# GitHub Configuration (Uses environment variables for security)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = "getblall/Lumeni"
FILE_PATH = "knowledge_base.txt"
BRANCH = "main"

# Detect if the environment is a GitHub Actions runner
IS_GITHUB_ACTION = os.environ.get("GITHUB_ACTIONS") == "true"

def push_to_github(new_logs_list):
    """Fetches knowledge_base.txt, appends new logs, and commits back to GitHub."""
    if not GITHUB_TOKEN:
        print("Sync aborted: GITHUB_TOKEN environment variable is missing.")
        return False

    url = f"https://github.com{GITHUB_REPO}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 1. Fetch current file to get its content and unique SHA blob
    response = requests.get(url, headers=headers)
    current_sha = None
    current_content = ""

    if response.status_code == 200:
        file_data = response.json()
        current_sha = file_data["sha"]
        current_content = base64.b64decode(file_data["content"]).decode("utf-8")
    elif response.status_code == 404:
        print("knowledge_base.txt not found on GitHub. Creating a fresh file.")
    else:
        print(f"Failed to fetch from GitHub (Status {response.status_code}): {response.text}")
        return False

    # 2. Append the batch of new math calculations
    log_string = "\n".join(new_logs_list)
    updated_content = current_content + "\n" + log_string
    encoded_content = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")

    # 3. Commit changes back to the repository
    payload = {
        "message": f"🤖 Lumeni Sync: Batched {len(new_logs_list)} autonomous calculations",
        "content": encoded_content,
        "branch": BRANCH
    }
    if current_sha:
        payload["sha"] = current_sha

    put_response = requests.put(url, headers=headers, json=payload)
    
    is_success_200 = bool(put_response.status_code == 200)
    is_success_201 = bool(put_response.status_code == 201)
    
    if is_success_200 or is_success_201:
        print(f"Successfully synced {len(new_logs_list)} calculations to GitHub!")
        return True
    else:
        print(f"Failed to commit to GitHub (Status {put_response.status_code}): {put_response.text}")
        return False

def lumeni_engine_loop():
    """Generates math logs and batch syncs them to GitHub."""
    print("Lumeni SymPy Engine initiated...")
    while True:
        batch_logs = []
        
        # Run a burst cycle to collect ~15 clean calculations
        for _ in range(15):
            try:
                # --- Advanced Math Generation via SymPy ---
                x = sp.Symbol('x')
                expr = x**2 + 3*x + 2
                diff_expr = sp.diff(expr, x)
                log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] f(x)={expr} | f'(x)={diff_expr}"
                # -------------------------------------------
                
                batch_logs.append(log_entry)
                time.sleep(1)  # Sped up processing pace slightly for faster execution
            except Exception as e:
                print(f"Engine Error: {e}")

        # Sync the entire batch to GitHub
        if batch_logs:
            push_to_github(batch_logs)
            
        # ENVIRONMENT CHECK: If running as a GitHub Action workflow, close cleanly instead of looping infinitely
        if IS_GITHUB_ACTION:
            print("GitHub Action processing loop complete. Exiting cleanly.")
            sys.exit(0)
            
        print("Window completed. Pausing engine...")
        time.sleep(60)

# Start execution depending on environment type (Render vs GitHub Actions)
if __name__ == '__main__':
    if HAS_FLASK:
        # We are on Render: Launch math engine in background thread, serve Flask on main thread
        engine_thread = threading.Thread(target=lumeni_engine_loop, daemon=True)
        engine_thread.start()
        
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        # We are in GitHub Actions: Execute the loop directly to write out data, then terminate cleanly
        lumeni_engine_loop()
