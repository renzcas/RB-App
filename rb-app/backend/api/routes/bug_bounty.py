from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database.session import get_db
from core.security.auth import require_role
from services.progress_service import ProgressService
from core.logging.audit import log_action

router = APIRouter()
progress = ProgressService()

# -------------------------
# Recon Labs
# -------------------------
@router.get("/recon/{lab_name}")
def run_recon(lab_name: str, user=Depends(require_role("student")), db: Session = Depends(get_db)):
    log_action(db, user["username"], "run_recon", lab_name)
    progress.mark_completed(db, user["username"], "lab", lab_name)

    return {"lab": lab_name, "status": "completed"}


# -------------------------
# Modules
# -------------------------
@router.get("/modules/{module_id}")
def run_module(module_id: int, user=Depends(require_role("student")), db: Session = Depends(get_db)):
    log_action(db, user["username"], "run_module", str(module_id))
    progress.mark_completed(db, user["username"], "module", str(module_id))

    return {"module": module_id, "status": "completed"}


# -------------------------
# Writeup Generator
# -------------------------
@router.get("/writeup")
def generate_writeup(vuln: str, endpoint: str, impact: str, user=Depends(require_role("student")), db: Session = Depends(get_db)):
    log_action(db, user["username"], "generate_writeup", vuln)

    writeup = f"""
Vulnerability: {vuln}
Endpoint: {endpoint}
Impact: {impact}

Summary:
The vulnerability allows an attacker to manipulate or access sensitive functionality.

Recommendation:
Validate inputs, sanitize user data, and enforce strict access controls.
"""

    return {"writeup": writeup.strip()}
