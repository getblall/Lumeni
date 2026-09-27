# PROD_BUILD_V7: Fully normalized Bearer auth vectors for absolute API conformity
import os
import sys
import subprocess
import random

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

# GitHub Configuration
GITHUB_TOKEN = (
    os.environ.get("GITHUB_TOKEN") or 
    os.environ.get("INPUT_GITHUB_TOKEN") or 
    os.environ.get("ACTIONS_RUNTIME_TOKEN")
)
BRANCH = "main"

# Detect if the environment is a GitHub Actions runner
IS_GITHUB_ACTION = os.environ.get("GITHUB_ACTIONS") == "true"

def push_to_github(new_logs_list):
    """Fetches knowledge_base.txt, appends new logs, and commits back to GitHub."""
    global GITHUB_TOKEN
    
    if not GITHUB_TOKEN:
        print("❌ Sync aborted: GITHUB_TOKEN environment variable is completely empty/missing.")
        return False

    target_api_url = "https://github.com"
    
    # FIXED AUTHORIZATION VECTOR: Switched completely to Bearer token format to satisfy GitHub API rules
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "User-Agent": "LumeniMathEngine-v7.0",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        # 1. Fetch current file to get its content and unique SHA blob
        response = requests.get(target_api_url, headers=headers)
        current_sha = None
        current_content = ""

        if response.status_code == 200:
            file_data = response.json()
            current_sha = file_data["sha"]
            current_content = base64.b64decode(file_data["content"]).decode("utf-8")
        elif response.status_code == 404:
            print("📝 Initializing a fresh target file.")
        else:
            print(f"❌ Failed to fetch from GitHub (Status {response.status_code}): {response.text}")
            return False

        # 2. Append the batch of new math calculations
        log_string = "\n".join(new_logs_list)
        updated_content = current_content + "\n" + log_string if current_content else log_string
        
        encoded_content_str = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")

        # 3. Commit changes back to the repository
        payload = {
            "message": "🤖 Lumeni Sync: Batched autonomous calculations",
            "content": encoded_content_str,
            "branch": BRANCH
        }
        if current_sha:
            payload["sha"] = current_sha

        put_response = requests.put(target_api_url, headers=headers, json=payload)
        
        is_success_200 = bool(put_response.status_code == 200)
        is_success_201 = bool(put_response.status_code == 201)
        
        if is_success_200 or is_success_201:
            print(f"✅ Successfully synced {len(new_logs_list)} calculations to GitHub knowledge base!")
            return True
        else:
            print(f"❌ Failed to commit to GitHub (Status {put_response.status_code}): {put_response.text}")
            return False
            
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Network Transaction Exception encountered: {req_err}")
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
        size = random.choice([2, 3])
        matrix_data = [[random.randint(-5, 5) for _ in range(size)] for _ in range(size)]
        M = sp.Matrix(matrix_data)
        
        if operation == "determinant":
            return f"[MATRIX - DET] det({matrix_data}) = {M.det()}"
        elif operation == "inverse" and M.det() != 0:
            return f"[MATRIX - INV] inv({matrix_data}) = M.inv().tolist()"
        else:
            return f"[MATRIX - EIGEN] eigenvalues({matrix_data}) = {M.eigenvals()}"

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
    batch_logs = []
    
    print("🔢 Commencing autonomous math compilation window...")
    for i in range(15):
        try:
            log_entry = generate_autonomous_math()
            timestamped_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {log_entry}"
            batch_logs.append(timestamped_entry)
            print(f"   [Math Log {i+1}/15 Generated Successfully]")
            time.sleep(0.1) 
        except Exception as e:
            print(f"⚠️ Engine Processing Exception: {e}")

    # Sync the entire batch to GitHub
    if batch_logs:
        push_to_github(batch_logs)
    else:
        print("⚠️ Sync skipped: No clean calculations were generated.")
        
    if IS_GITHUB_ACTION:
        print("🏁 GitHub Action processing loop complete. Exiting cleanly.")
        sys.exit(0)
        
    while True:
        print("Window completed. Pausing engine loop process...")
        time.sleep(60)

if __name__ == '__main__':
    if HAS_FLASK:
        engine_thread = threading.Thread(target=lumeni_engine_loop, daemon=True)
        engine_thread.start()
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        lumeni_engine_loop()
