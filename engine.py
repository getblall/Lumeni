# PROD_BUILD_AUTOPILOT_FINAL_V16: Standardized Python HTTP payload sync channel
import os
import sys
import subprocess
import random
import json
import base64
import time
import threading

# Force install standard network components if missing
try:
    import sympy as sp
except ImportError:
    print("Core dependency 'sympy' missing. Installing automatically...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sympy"])
    import sympy as sp

try:
    import requests
except ImportError:
    print("Core dependency 'requests' missing. Installing automatically...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

try:
    from flask import Flask
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    print("Flask module not detected. Proceeding in headless mode...")

if HAS_FLASK:
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Lumeni Engine is fully operational and syncing on autopilot.", 200

# Configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
FILE_PATH = "knowledge_base.txt"

def push_to_github_via_api(new_logs_list):
    """Updates knowledge_base.txt directly using Python HTTP handshakes, avoiding Render's broken terminal Git settings."""
    global GITHUB_TOKEN
    if not GITHUB_TOKEN:
        print("❌ BACKGROUND SYNC ERROR: GITHUB_TOKEN environment variable is completely empty or missing on Render!")
        return False

    print(f"🔄 BACKGROUND WORKER: Initializing HTTP payload synchronization for {len(new_logs_list)} items...")
    
    # Static API endpoint link
    target_api_url = "https://github.com"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "LumeniCoreEngineApp-v16.0"
    }

    try:
        # Step 1: Read the existing file content to grab its unique SHA code
        response = requests.get(target_api_url, headers=headers)
        current_sha = None
        current_content = ""

        if response.status_code == 200:
            file_data = response.json()
            current_sha = file_data.get("sha")
            current_content = base64.b64decode(file_data.get("content", "")).decode("utf-8")
            print("📂 Located existing tracking database file on GitHub.")
        elif response.status_code == 404:
            print("📝 Target file not found. Initializing a fresh knowledge container.")
        else:
            print(f"❌ Failed to reach GitHub gateway (Status {response.status_code}): {response.text}")
            return False

        # Step 2: Append your brand-new advanced math calculations
        log_string = "\n".join(new_logs_list)
        if current_content:
            updated_content = current_content + "\n" + log_string
        else:
            updated_content = log_string
            
        encoded_content_str = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")

        # Step 3: Package payload parameters into a clean dictionary map
        payload = {
            "message": "🤖 Lumeni Sync: Batched autonomous calculations",
            "content": encoded_content_str,
            "branch": "main"
        }
        if current_sha:
            payload["sha"] = current_sha

        # Step 4: Dispatch mutated updates straight to the repository branch endpoint
        put_response = requests.put(target_api_url, headers=headers, json=payload)
        
        if put_response.status_code == 200 or put_response.status_code == 201:
            print("✅ BACKGROUND WORKER SUCCESS: SUCCESSFULLY SYNCED BATCH GENERATIONS TO GITHUB ON AUTOPILOT!")
            return True
        else:
            print(f"❌ Gateway transaction rejected with Code {put_response.status_code}")
            print(f"ℹ️ Gateway Server Details: {put_response.text}")
            return False

    except Exception as e:
        print(f"❌ Critical connection framework transaction fault encountered: {e}")
        return False

def generate_autonomous_math():
    """Generates complex, randomized mathematical entries using SymPy."""
    category = random.choice(["calculus", "matrix", "algebra"])
    x, y = sp.symbols('x y')
    
    if category == "calculus":
        operation = random.choice(["derivative", "integral", "limit"])
        coeff1 = random.randint(2, 9)
        coeff2 = random.randint(1, 5)
        power = random.randint(3, 6)
        
        if operation == "derivative":
            expr = coeff1 * x**power - coeff2 * sp.sin(x)
            ans = sp.diff(expr, x)
            return f"[CALCULUS - DERIVATIVE] d/dx({expr}) = {ans}"
        elif operation == "integral":
            expr = coeff1 * x**(power-2) + coeff2 * sp.exp(x)
            ans = sp.integrate(expr, x)
            return f"[CALCULUS - INTEGRAL] ∫({expr}) dx = {ans} + C"
        else:
            expr = sp.sin(coeff1 * x) / (coeff2 * x)
            ans = sp.limit(expr, x, 0)
            return f"[CALCULUS - LIMIT] lim(x->0) [{expr}] = {ans}"

    elif category == "matrix":
        operation = random.choice(["determinant", "inverse", "eigenvalues"])
        size_choices = (2, 3)
        size = random.choice(size_choices)
        
        M = sp.matrices.dense.randMatrix(size, size, min=-5, max=5)
        
        if operation == "determinant":
            return f"[MATRIX - DET] det({M.tolist()}) = {M.det()}"
        elif operation == "inverse" and M.det() != 0:
            return f"[MATRIX - INV] inv({M.tolist()}) = {M.inv().tolist()}"
        else:
            return f"[MATRIX - EIGEN] eigenvalues({M.tolist()}) = {M.eigenvals()}"

    else:  # algebra
        operation = random.choice(["expand", "factor", "roots"])
        r1, r2 = random.randint(-4, 4), random.randint(-4, 4)
        
        if operation == "expand":
            expr = (x + r1) * (y - r2) * (x + 2)
            return f"[ALGEBRA - EXPAND] ({expr}) = {sp.expand(expr)}"
        elif operation == "factor":
            poly = sp.expand((x - r1) * (x - r2))
            return f"[ALGEBRA - FACTOR] {poly} = {sp.factor(poly)}"
        else:
            poly = x**2 - (r1 + r2)*x + (r1 * r2)
            return f"[ALGEBRA - ROOTS] roots({poly} = 0) => {sp.solve(poly, x)}"

def lumeni_engine_loop():
    """Generates advanced math logs and batch syncs them to GitHub."""
    print("Lumeni SymPy Engine initiated...")
    
    while True:
        batch_logs = []
        print("🔢 BACKGROUND WORKER: Commencing autonomous math compilation window...")
        
        for i in range(15):
            try:
                log_entry = generate_autonomous_math()
                timestamped_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {log_entry}"
                batch_logs.append(timestamped_entry)
                print(f"   [Math Log {i+1}/15 Generated Successfully]")
                time.sleep(0.2) 
            except Exception as e:
                print(f"⚠️ Engine Processing Exception: {e}")

        # Sync the entire batch to GitHub
        if batch_logs:
            push_to_github_via_api(batch_logs)
        else:
            print("⚠️ Sync skipped: No clean calculations were generated.")
            
        print("Window completed. Pausing engine loop process for 60 seconds...")
        time.sleep(60)

if __name__ == '__main__':
    if HAS_FLASK:
        engine_thread = threading.Thread(target=lumeni_engine_loop, daemon=True)
        engine_thread.start()
        
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        lumeni_engine_loop()
