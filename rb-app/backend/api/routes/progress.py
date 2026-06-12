from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database.session import get_db
from services.progress_service import ProgressService
from core.security.auth import require_role

router = APIRouter()
service = ProgressService()

@router.get("/my-progress")
def my_progress(user=Depends(require_role("student")), db: Session = Depends(get_db)):
    return service.get_user_progress(db, user["username"])
