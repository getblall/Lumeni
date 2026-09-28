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

# -------------------------------------------------------------------------
# 2. AUTONOMOUS MATHEMATICAL GENERATION ENGINE (SymPy Logic Container)
# -------------------------------------------------------------------------
def generate_math_assertion():
    """Generates a single advanced mathematical proof assertion using SymPy."""
    categories = ['calculus', 'linear_algebra', 'algebra']
    chosen_cat = random.choice(categories)
    x, y = sp.symbols('x y')
    
    if chosen_cat == 'calculus':
        sub = random.choice(['derivative', 'integral', 'limit'])
        if sub == 'derivative':
            expr = random.choice([sp.sin(x)*sp.exp(x), x**3 - 5*x**2 + 2, sp.log(x**2 + 1)])
            diff_expr = sp.diff(expr, x)
            return f"Calculus Derivative: The derivative of {expr} with respect to x is equal to {diff_expr}."
        elif sub == 'integral':
            expr = random.choice([x**2, sp.cos(x), sp.exp(-x)])
            int_expr = sp.integrate(expr, x)
            return f"Calculus Integral: The indefinite integral of {expr} with respect to x is equal to {int_expr} + C."
        else:
            expr = sp.sin(x)/x
            lim_val = sp.limit(expr, x, 0)
            return f"Calculus Limit: The limit of {expr} as x approaches 0 is equal to {lim_val}."
            
    elif chosen_cat == 'linear_algebra':
        sub = random.choice(['determinant', 'inverse'])
        if sub == 'determinant':
            a, b, c, d = random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5)
            M = sp.Matrix([[a, b], [c, d]])
            det = M.det()
            return f"Linear Algebra Matrix: The determinant of 2x2 matrix {M.tolist()} is equal to {det}."
        else:
            # Generate a guaranteed invertible 2x2 square matrix
            skew_val = random.randint(1, 5)
            M = sp.Matrix([[1, skew_val], [0, 1]])
            M_inv = M.inv()
            return f"Linear Algebra Matrix: The inverse of square matrix {M.tolist()} is equal to {M_inv.tolist()}."
            
    else:
        sub = random.choice(['expand', 'roots'])
        if sub == 'expand':
            expr = (x + random.randint(1, 5))**random.randint(2, 4)
            expanded = sp.expand(expr)
            return f"Algebra Expansion: Expanding the expression {expr} results structurally in {expanded}."
        else:
            a = random.randint(1, 3)
            b = random.randint(-5, 5)
            expr = a*x + b
            roots = sp.solve(expr, x)
            return f"Algebra Roots: The real roots solved for the equation {expr} = 0 evaluate to {roots}."

def background_math_engine_loop():
    """Compiles batches of 15 advanced mathematical assertions every 60 seconds."""
    print("[SYSTEM ENGINE] Autonomous SymPy computational engine loop started successfully.", flush=True)
    endpoint = f"{SUPABASE_URL}/rest/v1/math_logs"
    
    active_column_key = "assertion"
    try:
        probe_headers = {**HEADERS, "Range": "0-0"}
        probe_response = requests.get(endpoint, headers=probe_headers)
        if probe_response.status_code == 200:
            res_data = probe_response.json()
            if isinstance(res_data, list) and len(res_data) > 0:
                sample_row = res_data[0]
                for key in sample_row.keys():
                    if key not in ['id', 'created_at', 'timestamp']:
                        active_column_key = key
                        print(f"[SYSTEM ENGINE] Auto-Discovery successful! Detected live database column: '{active_column_key}'", flush=True)
                        break
    except Exception as e:
        print(f"[SYSTEM ENGINE] Auto-Discovery probe skipped, using fallback keys: {e}", flush=True)

    while True:
        try:
            print("[SYSTEM ENGINE] Computing fresh batch of 15 mathematical assertions...", flush=True)
            payload_batch = []
            
            for _ in range(15):
                assertion_string = generate_math_assertion()
                payload_batch.append({active_column_key: assertion_string})
            
            response = requests.post(endpoint, headers=HEADERS, json=payload_batch)
            
            if response.status_code == 201:
                print(f"[SYSTEM ENGINE] Batch processing successful! 15 assertions appended to cloud storage using key '{active_column_key}'.", flush=True)
            elif response.status_code == 400 and "PGRST204" in response.text:
                print(f"[SYSTEM ENGINE] Schema cache mismatch. Cycling production backup column identifiers...", flush=True)
                fallback_keys = ["Assertion", "text", "log", "math_log", "content"]
                for candidate_key in fallback_keys:
                    retry_batch = [{candidate_key: item[active_column_key]} for item in payload_batch]
                    retry_response = requests.post(endpoint, headers=HEADERS, json=retry_batch)
                    if retry_response.status_code == 201:
                        print(f"[SYSTEM ENGINE] Connection Restored! Switched active tracking column to: '{candidate_key}'", flush=True)
                        active_column_key = candidate_key
                        break
            else:
                print(f"[SYSTEM ENGINE] Database pipe warning. Status code returned: {response.status_code}. Response: {response.text}", flush=True)
                
        except Exception as e:
            print(f"[SYSTEM ENGINE] Processing error encountered inside runtime thread container: {e}", flush=True)
            
        time.sleep(60)

# -------------------------------------------------------------------------
# 3. WEB DASHBOARD PLATFORM ROUTES (Render Sleep Proof)
# -------------------------------------------------------------------------
@app.route('/')
def dashboard_home():
    """Queries public headers to present global state metrics on the live screen."""
    endpoint = f"{SUPABASE_URL}/rest/v1/math_logs"
    
    count_headers = {
        **HEADERS,
        "Prefer": "count=exact",
        "Range": "0-0"
    }
    
    try:
        response = requests.get(endpoint, headers=count_headers)
        content_range = response.headers.get("Content-Range", "")
        if "/" in content_range:
            total_assertions = content_range.split("/")[-1]
        else:
            total_assertions = "Unknown"
    except Exception as e:
        print(f"[WEB ERROR] Failed to fetch total record schema estimations: {e}", flush=True)
        total_assertions = "Error Connecting"

    html_layout = f"""
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
            hr {{ border: 0; border-top: 1px solid #374151; margin: 25px 0; }}
            a.btn {{ display: inline-block; background: #1f2937; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 4px; border: 1px solid #4b5563; font-weight: bold; }}
            a.btn:hover {{ background: #374151; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="status-line">🤖 Lumeni Math Core Status: <span class="green">ACTIVE</span></div>
            <div class="status-line">📍 Storage Method: <span class="cyan">Persistent Cloud Database (Render Sleep Proof)</span></div>
            <div class="status-line">📈 Total Mathematical Assertions Saved: <span class="green">{total_assertions} assertions</span></div>
            <hr>
            👉 <a class="btn" href="/download">[CLICK HERE TO STREAM AND SAVE YOUR FULL KNOWLEDGE_BASE.TXT FILE]</a>
        </div>
    </body>
    </html>
    """
    return html_layout

@app.route('/download')
def stream_download_knowledge_base():
    """Streams the complete cloud database history to the client browser text console."""
    endpoint = f"{SUPABASE_URL}/rest/v1/math_logs"
    
    try:
        response = requests.get(endpoint, headers=HEADERS)
        if response.status_code != 200:
            return f"Error downloading dataset: Supabase endpoint returned status code {response.status_code}"
            
        database_rows = response.json()
    except Exception as network_err:
        return f"Error connecting to cloud storage stream: {network_err}"

    output_lines = [
        "==================================================\n",
        "LUMENI AUTOMATED MATHEMATICAL LOG KNOWLEDGE BASE\n",
        f"Generated Extraction Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
        "==================================================\n\n"
    ]
    
    seen_assertions = set()
    for row in database_rows:
        row_fingerprint = str(row)
        if row_fingerprint not in seen_assertions:
            seen_assertions.add(row_fingerprint)
            
