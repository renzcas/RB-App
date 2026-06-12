from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database.session import get_db
from core.security.auth import require_role
from services.dashboard_service import DashboardService

router = APIRouter()
service = DashboardService()

@router.get("/user")
def user_dashboard(user=Depends(require_role("student")), db: Session = Depends(get_db)):
    stats = service.get_user_stats(db, user["username"])
    activity = service.get_recent_activity(db, user["username"])
    return {
        "stats": stats,
        "recent_activity": activity
    }
