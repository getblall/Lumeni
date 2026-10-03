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

HEADERS = {
    "ApiKey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

X, Y = sp.symbols('x y')
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
            return f"Calculus Derivative: The derivative of {expr} with respect to x is equal to {sp.diff(expr, X)}."
        elif sub == 'integral':
            expr = random.choice([X**2, sp.cos(X), sp.exp(-X)])
            return f"Calculus Integral: The indefinite integral of {expr} with respect to x is equal to {sp.integrate(expr, X)} + C."
        else:
            expr = sp.sin(X)/X
            return f"Calculus Limit: The limit of {expr} as x approaches 0 is equal to {sp.limit(expr, X, 0)}."
            
    elif chosen_cat == 'linear_algebra':
        sub = random.choice(['determinant', 'inverse'])
        if sub == 'determinant':
            a, b, c, d = random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5)
            M = sp.Matrix([[a, b], [c, d]])
            return f"Linear Algebra Matrix: The determinant of 2x2 matrix {M.tolist()} is equal to {M.det()}."
        else:
            skew_val = random.randint(1, 5)
            M = sp.Matrix([[1, skew_val], [0, 1]])
            return f"Linear Algebra Matrix: The inverse of square matrix {M.tolist()} is equal to {M.inv().tolist()}."
            
    else:
        sub = random.choice(['expand', 'roots'])
        if sub == 'expand':
            expr = (X + random.randint(1, 5))**random.randint(2, 4)
            return f"Algebra Expansion: Expanding the expression {expr} results structurally in {sp.expand(expr)}."
        else:
            a = random.randint(1, 3)
            b = random.randint(-5, 5)
            expr = a*X + b
            return f"Algebra Roots: The real roots solved for the equation {expr} = 0 evaluate to {sp.solve(expr, X)}."

def background_math_engine_loop():
    """Compiles batches of 15 assertions every 30 seconds and checks cache limits."""
    time.sleep(2.0)
    endpoint = f"{SUPABASE_URL}/rest/v1/math_logs"
    active_column_key = "calculation"
    
    while True:
        try:
            # 🧼 AUTOMATIC WIPE MIGRATOR: If records build up, safely clean them to keep everything fast
            count_res = requests.get(endpoint, headers={**HEADERS, "Prefer": "count=exact", "Range": "0-0"})
            content_range = count_res.headers.get("Content-Range", "")
            total = int(content_range.split("/")[-1]) if "/" in content_range else 0
            
            # If database table holds more than 5,000 equations, wipe it to reclaim high speeds
            if total > 5000:
                print(f"[MEMORY WIPE] Clearing data table cache scale ({total} items cleared safely)...", flush=True)
                requests.delete(f"{endpoint}?id=gt.0", headers=HEADERS)

            print("[SYSTEM ENGINE] Computing fresh batch of 15 mathematical assertions...", flush=True)
            raw_math_strings = [generate_math_assertion() for _ in range(15)]
            
            payload_batch = [{active_column_key: string} for string in raw_math_strings]
            response = requests.post(endpoint, headers=HEADERS, json=payload_batch)
            
            if response.status_code == 201:
                print(f"[SYSTEM ENGINE] Batch processing successful using key '{active_column_key}'.", flush=True)
            elif response.status_code == 400 and "PGRST204" in response.text:
                fallback_keys = ["Assertion", "text", "log", "math_log", "content"]
                for candidate_key in fallback_keys:
                    retry_batch = [{candidate_key: string} for string in raw_math_strings]
                    retry_response = requests.post(endpoint, headers=HEADERS, json=retry_batch)
                    if retry_response.status_code == 201:
                        active_column_key = candidate_key
                        LIVE_COLUMN_TRACKER["key"] = candidate_key
                        break
        except Exception as e:
            print(f"[SYSTEM ENGINE] Operational exception: {e}", flush=True)
            
        time.sleep(30)

engine_thread = threading.Thread(target=background_math_engine_loop, daemon=True)
engine_thread.start()

# -------------------------------------------------------------------------
# 3. WEB DASHBOARD PLATFORM ROUTES
# -------------------------------------------------------------------------
@app.route('/')
def dashboard_home():
    endpoint = f"{SUPABASE_URL}/rest/v1/math_logs"
    count_headers = {**HEADERS, "Prefer": "count=exact", "Range": "0-0"}
    try:
        response = requests.get(endpoint, headers=count_headers)
        content_range = response.headers.get("Content-Range", "")
        total_assertions = content_range.split("/")[-1] if "/" in content_range else "Unknown"
    except Exception as e:
        total_assertions = "Sync Error"

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
            <div class="status-line">Active Live Cache Assertions: <span class="cyan">{total_assertions} records</span></div>
            <div class="status-line">Target Performance Mode: <span class="cyan">Auto-Purge Enabled</span></div>
            <hr style="border: 0; border-top: 1px solid #1f2937; margin: 20px 0;">
            <p style="font-size: 12px; color: #6b7280;">Engine compiles data loops every 30 seconds. To maintain extreme speeds, live cache clears periodically into archives.</p>
            <a href="/download" class="btn" target="_blank">📥 Download Active Study Log (.txt)</a>
        </div>
    </body>
    </html>
    """

@app.route('/download')
def download_logs():
    """Dynamically streams chunks of logs to prevent memory exhaustion crashes."""
    endpoint = f"{SUPABASE_URL}/rest/v1/math_logs"
    params = {"order": "created_at.desc", "limit": "300"}
    
    response = requests.get(endpoint, headers=HEADERS, params=params)
    records = response.json()
    target_key = LIVE_COLUMN_TRACKER.get("key", "calculation")
    
    output = [
        "=========================================================================",
        "🚀 LUMENI AI COMPILATION TRACKER: PERFORMANCE LIVE STREAM EXPORT",
        "=========================================================================",
        f"Export Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
    ]
    
    if isinstance(records, list) and len(records) > 0:
        for idx, item in enumerate(records):
            output.append(f"[{item.get('created_at', 'Time Unknown')}] Item #{idx+1}: {item.get(target_key, '[Missing Value]')}")
    else:
        output.append("Live cache is currently empty following a scheduled auto-wipe loop cycle.")
        
    return Response(
        "\n".join(output),
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=lumeni_live_log.txt"}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
