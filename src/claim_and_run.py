import os, hashlib, requests
from datetime import datetime, timezone

RUN_KEY = "clone-handoff-001"
INSTANCE_ID = "instance-B-local-codex"
URL = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
H = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

def get_handoff():
    r = requests.get(f"{URL}/rest/v1/instance_handoff",
        params={"run_key": f"eq.{RUN_KEY}", "select": "*"}, headers=H, timeout=20)
    r.raise_for_status()
    rows = r.json()
    if not rows: raise RuntimeError("handoff not found")
    return rows[0]

def claim():
    r = requests.post(f"{URL}/rest/v1/rpc/claim_instance_handoff",
        json={"p_run_key": RUN_KEY, "p_instance_id": INSTANCE_ID},
        headers=H, timeout=20)
    r.raise_for_status()
    return r.json()

before = get_handoff()
print("Observed:", before)
if before["task_status"] != "waiting_for_successor":
    raise SystemExit("NOT CLAIMED: task is not waiting_for_successor")

print("Claim:", claim())
after = get_handoff()
print("After claim:", after)

if not (after.get("task_status") == "claimed" and after.get("claimed_by") == INSTANCE_ID):
    raise SystemExit("CLAIM FAILED")

result = "Independent local successor B executed the handoff task at " + datetime.now(timezone.utc).isoformat()
digest = hashlib.sha256(result.encode()).hexdigest()

r = requests.patch(f"{URL}/rest/v1/instance_handoff",
    params={"run_key": f"eq.{RUN_KEY}"},
    json={"task_status": "completed", "result": result, "result_digest": digest},
    headers={**H, "Prefer": "return=representation"}, timeout=20)
r.raise_for_status()
print("Final:", get_handoff())
print("SUCCESS: local B claimed and completed the handoff.")
