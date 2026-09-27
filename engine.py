# PROD_BUILD_V12: Stripped explicit branch fields to avoid Content Routing 404 Errors
import os
import sys
import subprocess
import random
import json
import base64
import time
import threading

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
IS_GITHUB_ACTION = os.environ.get("GITHUB_ACTIONS") == "true"

def push_to_github(new_logs_list):
    """Fetches and updates knowledge_base.txt using native OS curl commands to completely bypass 406 blocks."""
    if not GITHUB_TOKEN:
        print("❌ Sync aborted: GITHUB_TOKEN environment variable is missing.")
        return False

    target_url = "https://github.com"
    print(f"🔄 Processing file sync operations using OS curl pipeline layout...")

    current_sha = None
    current_content = ""

    # Step 1: Use a clean curl command line string execution block to get the current file and SHA
    cmd_get = [
        "curl", "-s", "-X", "GET", target_url,
        "-H", f"Authorization: token {GITHUB_TOKEN}",
        "-H", "Accept: application/vnd.github.v3+json",
        "-H", "User-Agent: LumeniCoreEngine"
    ]
    
    try:
        result_get = subprocess.run(cmd_get, capture_output=True, text=True, check=True)
        
        if result_get.stdout and result_get.stdout.strip():
            try:
                data = json.loads(result_get.stdout)
                if isinstance(data, dict):
                    if "sha" in data:
                        current_sha = data["sha"]
                        current_content = base64.b64decode(data["content"]).decode("utf-8")
                        print("📂 Found existing knowledge_base.txt file via curl.")
                    elif data.get("message") == "Not Found" or "not found" in str(data.get("message")).lower():
                        print("📝 knowledge_base.txt not found on GitHub. Starting a fresh file build.")
                    else:
                        # Catch hidden tracking messages
                        if "message" in data:
                            print(f"ℹ️ Status context feedback message: {data['message']}")
            except json.JSONDecodeError:
                print("📝 Output is plain text or empty. Proceeding with fresh file write mapping context.")
        else:
            print("📝 Target file is completely blank. Initializing fresh tracking container layout.")
            
    except Exception as err:
        print(f"⚠️ System pipeline lookup exception caught: {err}. Proceeding with fresh initialization.")

    # Step 2: Append the batch of new math calculations
    log_string = "\n".join(new_logs_list)
    updated_content = current_content + "\n" + log_string if current_content else log_string
    encoded_content_str = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")

    # Step 3: Write payload data parameters to a temporary hidden directory file
    # FIXED: Stripped explicit branch parameters to let GitHub Actions resolve HEAD routing natively
    payload = {
        "message": "🤖 Lumeni Sync: Batched autonomous calculations",
        "content": encoded_content_str
    }
    if current_sha:
        payload["sha"] = current_sha

    with open("payload.json", "w") as f:
        json.dump(payload, f)

    # Step 4: Execute the PUT file sync write block via raw curl pointing to the payload file
    cmd_put = [
        "curl", "-s", "-X", "PUT", target_url,
        "-H", f"Authorization: token {GITHUB_TOKEN}",
        "-H", "Accept: application/vnd.github.v3+json",
        "-H", "User-Agent: LumeniCoreEngine",
        "-H", "Content-Type: application/json",
        "-d", "@payload.json"
    ]

    try:
        result_put = subprocess.run(cmd_put, capture_output=True, text=True, check=True)
        if result_put.stdout and result_put.stdout.strip():
            try:
                put_data = json.loads(result_put.stdout)
                if isinstance(put_data, dict) and ("content" in put_data or "commit" in put_data):
                    print("✅ Successfully synced calculations directly to GitHub knowledge base via curl pipeline!")
                    if os.path.exists("payload.json"):
                        os.remove("payload.json")
                    return True
                else:
                    print(f"❌ Gateway transaction rejected (Status check failed): {result_put.stdout}")
                    return False
            except json.JSONDecodeError:
                print(f"❌ Non-JSON gateway content received during put operation: {result_put.stdout}")
                return False
        else:
            print("❌ Received an absolute blank transaction response acknowledgment vector.")
            return False
    except Exception as put_err:
        print(f"❌ OS pipeline connection transaction failed: {put_err}")
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
        matrix_data = [[random.randint(-5, 5) for _ in range(size)] for _ in range(size)]
        M = sp.Matrix(matrix_data)
        
        if operation == "determinant":
            return f"[MATRIX - DET] det({matrix_data}) = {M.det()}"
        elif operation == "inverse" and M.det() != 0:
            return f"[MATRIX - INV] inv({matrix_data}) = {M.inv().tolist()}"
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
