# PROD_BUILD_LOCAL_AUTOPILOT: Native server disk logging to completely bypass GitHub API firewalls
import os
import sys
import subprocess
import random
import time
import threading

# Force install standard network components if missing inside the environment
try:
    import sympy as sp
except ImportError:
    print("Core dependency 'sympy' missing. Installing automatically...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sympy"])
    import sympy as sp

try:
    from flask import Flask, send_file
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    print("Flask module not detected. Proceeding in headless mode...")

# Local file configuration parameters
LOCAL_FILE_PATH = "local_knowledge_base.txt"

if HAS_FLASK:
    app = Flask(__name__)

    @app.route('/')
    def home():
        # Step 1: Read current compilation metrics
        total_logs = 0
        if os.path.exists(LOCAL_FILE_PATH):
            with open(LOCAL_FILE_PATH, "r", encoding="utf-8") as f:
                total_logs = len(f.readlines())
        
        # Step 2: Display an interactive, clean status screen directly on your Render URL link
        html_dashboard = f"""
        <html>
            <head><title>Lumeni Autonomous Engine</title></head>
            <body style="font-family: monospace; padding: 40px; background: #111; color: #0f0;">
                <h2>🤖 Lumeni Math Core Status: ACTIVE</h2>
                <p>📍 Storage Method: Local Server Disk File (GitHub API Defeated)</p>
                <p>📈 Total Mathematical Assertions Tracked: <strong>{total_logs} assertions</strong></p>
                <hr style="border-color: #0f0;">
                <p>👉 <a href="/download" style="color: #fff; font-weight: bold;">[CLICK HERE TO DOWNLOAD YOUR FULL KNOWLEDGE_BASE.TXT FILE]</a></p>
            </body>
        </html>
        """
        return html_dashboard, 200

    @app.route('/download')
    def download_file():
        """Allows you to download your entire math database straight out of the server via your web browser."""
        if os.path.exists(LOCAL_FILE_PATH):
            return send_file(LOCAL_FILE_PATH, as_attachment=True, download_name="knowledge_base.txt")
        return "Database file initialization window active. Please check back in a few minutes.", 404

def save_to_local_disk(new_logs_list):
    """Appends logs natively directly to the server's tracking file layout, completely bypassing GitHub's platform rules."""
    global LOCAL_FILE_PATH
    print(f"🔄 SYSTEM LOG WORKER: Appending {len(new_logs_list)} items directly to local server storage disk...")
    
    try:
        # Core Python disk write block - uses zero internet, zero tokens, and can never trigger a 404
        log_string = "\n".join(new_logs_list) + "\n"
        with open(LOCAL_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(log_string)
            
        print("✅ SYSTEM LOG WORKER SUCCESS: LOCALLY WRITTEN AND LOCKED ADVANCED MATH LOGS INTO SERVER DISK BASE!")
        return True
    except Exception as e:
        print(f"❌ LOCAL STORAGE EXCEPTION ENCOUNTERED: {e}")
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
    """Generates advanced math logs and batch syncs them to local storage disk."""
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

        # Save the batch straight to local server files
        if batch_logs:
            save_to_local_disk(batch_logs)
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
