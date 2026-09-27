# PROD_BUILD_FINAL_V14: Universal header authorization formatting normalization
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

# Dynamically handle Flask (Only required on Render, completely optional for GitHub Actions)
try:
    from flask import Flask
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    print("Flask module not detected. Proceeding in headless compiler mode...")

if HAS_FLASK:
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Lumeni Engine is fully operational and syncing on autopilot.", 200

# GitHub Configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
BRANCH = "main"
IS_GITHUB_ACTION = os.environ.get("GITHUB_ACTIONS") == "true"

def push_to_github(new_logs_list):
    """Fetches and updates knowledge_base.txt using native requests with normalized authorization headers."""
    if not GITHUB_TOKEN:
        print("❌ Sync aborted: GITHUB_TOKEN environment variable is missing.")
        return False

    target_url = "https://github.com"
    print("🔄 Initializing native API channel transaction pipelines...")

    # NORMALIZED HEADERS: Formatted explicitly to satisfy modern GitHub API connection gateway standards
    token_str = str(GITHUB_TOKEN).strip()
    if token_str.startswith("ghp_") or token_str.startswith("github_pat_"):
        auth_header = f"token {token_str}"
    else:
        auth_header = f"Bearer {token_str}"

    headers = {
        "Authorization": auth_header,
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "LumeniCoreEngineApp-v14.0"
    }

    current_sha = None
    current_content = ""

    # Step 1: Securely query current file target variables
    try:
        response = requests.get(target_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            current_sha = data.get("sha")
            current_content = base64.b64decode(data.get("content", "")).decode("utf-8")
            print("📂 Located existing tracking database file. Syncing content vectors...")
        elif response.status_code == 404 or response.status_code == 406:
            print("📝 Target tracking asset file context initialized. Creating a fresh knowledge container.")
        else:
            print(f"ℹ️ Handshake status response received: {response.status_code}")
    except Exception as read_err:
        print(f"⚠️ Exception handled during initial stream lookups: {read_err}")

    # Step 2: Append the batch of new math calculations
    log_string = "\n".join(new_logs_list)
    updated_content = current_content + "\n" + log_string if current_content else log_string
    encoded_content_str = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")

    # Step 3: Package payload parameters inside a fully closed structure wrapper map
    payload = {
        "message": "🤖 Lumeni Sync: Batched autonomous calculations",
        "content": encoded_content_str,
        "branch": BRANCH
    }
    if current_sha:
        payload["sha"] = current_sha

    # Step 4: Dispatch mutated updates straight to the repository branch endpoint
    try:
        put_response = requests.put(target_url, headers=headers, json=payload)
        
        is_200_ok = bool(put_response.status_code == 200)
        is_201_created = bool(put_response.status_code == 201)
        
        if is_200_ok or is_201_created:
            print(f"✅ SUCCESSFULLY SYNCED {len(new_logs_list)} ADVANCED MATH GENERATIONS TO GITHUB KNOWLEDGE BASE!")
            return True
        else:
            print(f"❌ Transmission interface transaction rejected with Code {put_response.status_code}")
            print(f"ℹ️ Gateway Server Details: {put_response.text}")
            return False
    except Exception as put_err:
        print(f"❌ Critical connection framework transaction fault encountered: {put_err}")
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

