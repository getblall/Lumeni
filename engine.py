import os
import time
import random
import threading
from flask import Flask, Response
import requests
import sympy as sp

# -------------------------------------------------------------------------
# 1. CORE SYSTEM ARCHITECTURE & ENVIRONMENT CONFIGURATION
# -------------------------------------------------------------------------
app = Flask(__name__)

PORT = int(os.environ.get("PORT", 10000))
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://supabase.co").strip()
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()

# Construct headers for standard PostgREST interactions
HEADERS = {
    "ApiKey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Pre-define global math symbols to conserve CPU cycles at 30s speeds
X, Y = sp.symbols('x y')

# Global variable to cache the live discovered column safely across threads
LIVE_COLUMN_TRACKER = {"key": "calculation"}

# -------------------------------------------------------------------------
# 2. AUTONOMOUS MATHEMATICAL GENERATION ENGINE (SymPy Logic Container)
# -------------------------------------------------------------------------
def generate_math_assertion():
    """Generates a single advanced mathematical proof assertion using SymPy."""
    categories = ['calculus', 'linear_algebra', 'algebra']
    chosen_cat = random.choice(categories)
    
    if chosen_cat == 'calculus':
        sub = random.choice(['derivative', 'integral', 'limit'])
        if sub == 'derivative':
            expr = random.choice([sp.sin(X)*sp.exp(X), X**3 - 5*X**2 + 2, sp.log(X**2 + 1)])
            diff_expr = sp.diff(expr, X)
            return f"Calculus Derivative: The derivative of {expr} with respect to x is equal to {diff_expr}."
        elif sub == 'integral':
            expr = random.choice([X**2, sp.cos(X), sp.exp(-X)])
            int_expr = sp.integrate(expr, X)
            return f"Calculus Integral: The indefinite integral of {expr} with respect to x is equal to {int_expr} + C."
        else:
            expr = sp.sin(X)/X
            lim_val = sp.limit(expr, X, 0)
            return f"Calculus Limit: The limit of {expr} as x approaches 0 is equal to {lim_val}."
            
    elif chosen_cat == 'linear_algebra':
        sub = random.choice(['determinant', 'inverse'])
        if sub == 'determinant':
            a, b, c, d = random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5)
            M = sp.Matrix([[a, b], [c, d]])
            det = M.det()
            return f"Linear Algebra Matrix: The determinant of 2x2 matrix {M.tolist()} is equal to {det}."
        else:
            # ✅ FIXED: Native square 2x2 matrix instantiation structure to prevent inversion runtime crashes
            skew_val = random.randint(1, 5)
            M = sp.Matrix([[1, skew_val], [0, 1]])
            M_inv = M.inv()
            return f"Linear Algebra Matrix: The inverse of square matrix {M.tolist()} is equal to {M_inv.tolist()}."
            
    else:
        sub = random.choice(['expand', 'roots'])
        if sub == 'expand':
            expr = (X + random.randint(1, 5))**random.randint(2, 4)
            expanded = sp.expand(expr)
            return f"Algebra Expansion: Expanding the expression {expr} results structurally in {expanded}."
        else:
            a = random.randint(1, 3)
            b = random.randint(-5, 5)
            expr = a*X + b
            roots = sp.solve(expr, X)
            return f"Algebra Roots: The real roots solved for the equation {expr} = 0 evaluate to {roots}."

def background_math_engine_loop():
    """Compiles batches of 15 advanced mathematical assertions every 30 seconds."""
    time.sleep(2.0)
    print("[SYSTEM ENGINE] Autonomous SymPy computational engine loop started successfully.", flush=True)
    endpoint = f"{SUPABASE_URL}/rest/v1/math_logs"
    
    active_column_key = "calculation"
    
    while True:
        try:
            print("[SYSTEM ENGINE] Computing fresh batch of 15 mathematical assertions...", flush=True)
            raw_math_strings = [generate_math_assertion() for _ in range(15)]
            
            payload_batch = [{active_column_key: string} for string in raw_math_strings]
            response = requests.post(endpoint, headers=HEADERS, json=payload_batch)
            
            if response.status_code == 201:
                print(f"[SYSTEM ENGINE] Batch processing successful! 15 assertions appended to cloud storage using key '{active_column_key}'.", flush=True)
            elif response.status_code == 400 and "PGRST204" in response.text:
                print(f"[SYSTEM ENGINE] Schema cache mismatch. Cycling production backup column identifiers...", flush=True)
                fallback_keys = ["Assertion", "text", "log", "math_log", "content"]
                
                connection_restored = False
                for candidate_key in fallback_keys:
                    retry_batch = [{candidate_key: string} for string in raw_math_strings]
                    retry_response = requests.post(endpoint, headers=HEADERS, json=retry_batch)
                    if retry_response.status_code == 201:
                        print(f"[SYSTEM ENGINE] Connection Restored! Switched active tracking column to: '{candidate_key}'", flush=True)
                        active_column_key = candidate_key
                        LIVE_COLUMN_TRACKER["key"] = candidate_key
                        connection_restored = True
                        break
                if not connection_restored:
                    print("[SYSTEM ENGINE] Critical Fallback Failure. All backup candidates rejected.", flush=True)
            else:
                print(f"[SYSTEM ENGINE] Database pipe warning. Status code returned: {response.status_code}. Response: {response.text}", flush=True)
                
        except Exception as e:
            print(f"[SYSTEM ENGINE] Processing error encountered inside runtime thread container: {e}", flush=True)
            
        time.sleep(30)

# Start background math engine worker thread automatically upon file inclusion
engine_thread = threading.Thread(target=background_math_engine_loop, daemon=True)
engine_thread.start()

# -------------------------------------------------------------------------
# 3. WEB DASHBOARD PLATFORM ROUTES (Render Sleep Proof)
# -------------------------------------------------------------------------
@app.route('/')
def dashboard_home():
    """Queries public headers to present global state metrics on the live screen."""
    endpoint = f"{SUPABASE_URL}/rest/v1/math_logs"
    count_headers = {**HEADERS, "Prefer": "count=exact", "Range": "0-0"}
    
    try:
        response = requests.get(endpoint, headers=count_headers)
        content_range = response.headers.get("Content-Range", "")
        total_assertions = content_range.split("/")[-1] if "/" in content_range else "Unknown"
    except Exception as e:
        print(f"[WEB ERROR] Failed to fetch total record schema estimations: {e}", flush=True)
        total_assertions = "Error Connecting"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lumeni Control Panel</title>
        <style>
            body {{ background-color: #0b0f19; color: #a9b2c3; font-family: 'Courier New', monospace; padding: 40px; line-height: 1.6; }}
            .container {{ max-width: 800px; margin: 0 auto; background: #111827; padding: 30px; border-radius: 8px; border: 1px solid #1f2937; }}
            .status-line {{ margin-bottom: 15px; font-size: 16px; font-weight: bold; }}
            .green {{ color: #10b981; }}
            .cyan {{ color: #06b6d4; }}
            .btn {{ display: inline-block; background-color: #2563eb; color: #ffffff; padding: 10px 20px; border-radius: 4px; text-decoration: none; font-weight: bold; margin-top: 15px; }}
            .btn:hover {{ background-color: #1d4ed8; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🚀 Lumeni AI Project Cluster</h2>
            <div class="status-line">Engine State: <span class="green">RUNNING (Thread-0)</span></div>
            <div class="status-line">Compiled Knowledge Assertions: <span class="cyan">{total_assertions} records</span></div>
            <div class="status-line">Target Data Pipe Interval: <span class="cyan">30 Seconds Loop</span></div>
            <hr style="border: 0; border-top: 1px solid #1f2937; margin: 20px 0;">
            <p style="font-size: 12px; color: #6b7280;">Engine continuously compiles 15 complex mathematical proofs every 30 seconds (~43,200 equations / day).</p>
            <a href="/download" class="btn" target="_blank">📥 Download Study Log (.txt)</a>
        </div>
    </body>
    </html>
    """

@app.route('/download')
def download_logs():
    """Queries recent items from Supabase and pipes them out into a raw text file download."""
    endpoint = f"{SUPABASE_URL}/rest/v1/math_logs"
    params = {"order": "created_at.desc", "limit": "100"}
    
    # ✅ FIXED: Flattened code block with no conditional try variations to completely bypass cross-platform spacing errors
    response = requests.get(endpoint, headers=HEADERS, params=params)
    records = response.json()
    target_key = LIVE_COLUMN_TRACKER.get("key", "calculation")
    
    output_buffer = []
    output_buffer.append("=========================================================================")
    output_buffer.append("🚀 LUMENI AI COMPILATION TRACKER: ACTIVE LIVE DATA EXPORT")
    output_buffer.append("=========================================================================")
    output_buffer.append(f"Export Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    
    if isinstance(records, list) and len(records) > 0:
        for index, item in enumerate(records):
            text_content = item.get(target_key, "[Column Key Mismatch]")
            timestamp = item.get("created_at", "Unknown Time")
