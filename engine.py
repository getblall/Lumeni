# PROD_BUILD_AUTOPILOT_FINAL_V15: Using native credential helper configurations to bypass all URL variables
import os
import sys
import subprocess
import random
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

def push_to_github_via_git(new_logs_list):
    """Appends logs locally and uses native Git configurations to handle tokens safely without dynamic strings."""
    global GITHUB_TOKEN
    if not GITHUB_TOKEN:
        print("❌ BACKGROUND SYNC ERROR: GITHUB_TOKEN environment variable is completely empty or missing on Render!")
        return False

    print(f"🔄 BACKGROUND WORKER: Initializing native Git tree synchronization sequence for {len(new_logs_list)} items...")
    
    try:
        # 1. Append the batch of math calculations to the local file
        log_string = "\n".join(new_logs_list) + "\n"
        with open(FILE_PATH, "a", encoding="utf-8") as f:
            f.write(log_string)
        print("📂 BACKGROUND WORKER: Appended calculations to local tracking container.")

        # 2. Configure Git identification parameters to prevent commit blocking flags
        subprocess.run(["git", "config", "user.name", "Lumeni Engine Bot"], check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "lumeni-bot@onrender.com"], check=True, capture_output=True)

        # 3. Stage the modified knowledge base file
        subprocess.run(["git", "add", FILE_PATH], check=True, capture_output=True)

        # 4. Commit the changes locally
        commit_msg = f"🤖 Lumeni Sync: Batched {len(new_logs_list)} autonomous calculations"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, capture_output=True)

        # 5. ABSOLUTE FIXED GIT AUTHENTICATION VECTOR:
        # No variables, no formatting, no f-strings inside the push command.
        # This pipes your token directly through a standard Git secure helper shell interface.
        clean_token = str(GITHUB_TOKEN).strip()
        
        # Tell Git to dynamically echo back the token password whenever the terminal requests it
        subprocess.run([
            "git", "config", "credential.helper", 
            f"!f() {{ echo username=oauth2; echo password={clean_token}; }}; f"
        ], check=True)

        # Execute push targeting a completely static, un-scrubbable repository path destination
        result_push = subprocess.run(
            ["git", "push", "https://github.com", "HEAD:main"], 
            capture_output=True, 
            text=True
        )

        # Unset the helper immediately after push execution completes for absolute safety
        subprocess.run(["git", "config", "--unset", "credential.helper"])

        if result_push.returncode == 0:
            print("✅ BACKGROUND WORKER SUCCESS: SUCCESSFULLY SYNCED BATCH GENERATIONS TO GITHUB ON AUTOPILOT!")
            return True
        else:
            print(f"❌ BACKGROUND SYNC REJECTED BY GITHUB: {result_push.stderr}")
            return False

    except subprocess.CalledProcessError as git_err:
        print(f"❌ BACKGROUND GIT PROCESS ERROR: {git_err.stderr}")
        return False
    except Exception as e:
        print(f"❌ BACKGROUND UNEXPECTED FAULT: {e}")
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
            push_to_github_via_git(batch_logs)
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
