import os
import time
import random
import requests
import sympy as sp

# -------------------------------------------------------------------------
# 1. CORE SYSTEM ARCHITECTURE & ENVIRONMENT CONFIGURATION
# -------------------------------------------------------------------------
print("[SYSTEM] Initializing Lumeni Autonomous Math Core...", flush=True)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://supabase.co").strip()
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()

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

def run_production_loop():
    """Compiles batches of 15 advanced mathematical assertions indefinitely."""
    endpoint = f"{SUPABASE_URL}/rest/v1/math_logs"
    print("[SYSTEM ENGINE] Pipeline loop connected to cloud database engine.", flush=True)
    
    # Simple direct string field layout target mapping
    active_column_key = "assertion"

    while True:
        try:
            print("[SYSTEM ENGINE] Computing fresh batch of 15 mathematical assertions...", flush=True)
            payload_batch = []
            
            for _ in range(15):
                assertion_string = generate_math_assertion()
                payload_batch.append({active_column_key: assertion_string})
            
            response = requests.post(endpoint, headers=HEADERS, json=payload_batch)
            
            if response.status_code == 201:
                print(f"[SYSTEM ENGINE] Batch processing successful! 15 assertions saved directly.", flush=True)
            elif response.status_code == 400 and "PGRST204" in response.text:
                fallback_keys = ["Assertion", "text", "log", "math_log", "content"]
                for candidate_key in fallback_keys:
                    retry_batch = [{candidate_key: item[active_column_key]} for item in payload_batch]
                    retry_response = requests.post(endpoint, headers=HEADERS, json=retry_batch)
                    if retry_response.status_code == 201:
                        active_column_key = candidate_key
                        print(f"[SYSTEM ENGINE] Layout Restored! Column locked to: '{candidate_key}'", flush=True)
                        break
            else:
                print(f"[SYSTEM ENGINE] Pipeline notice. Code: {response.status_code}. Data: {response.text}", flush=True)
                
        except Exception as e:
            print(f"[SYSTEM ENGINE] Loop processing error: {e}", flush=True)
            
        time.sleep(60)

# -------------------------------------------------------------------------
# 3. DIRECT FLOW SYSTEM INITIALIZATION
# -------------------------------------------------------------------------
if __name__ == '__main__':
    run_production_loop()
