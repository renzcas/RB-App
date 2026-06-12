from sqlalchemy.orm import Session
from core.database.models import Progress, AuditLog

class DashboardService:
    def get_user_stats(self, db: Session, username: str):
        modules = db.query(Progress).filter_by(username=username, item_type="module").all()
        labs = db.query(Progress).filter_by(username=username, item_type="lab").all()

        modules_completed = sum(1 for m in modules if m.completed)
        labs_completed = sum(1 for l in labs if l.completed)

        return {
            "modules_completed": modules_completed,
            "total_modules": 5,
            "labs_completed": labs_completed,
            "total_labs": 4,
            "module_progress_percent": (modules_completed / 5) * 100,
            "lab_progress_percent": (labs_completed / 4) * 100,
        }

    def get_recent_activity(self, db: Session, username: str):
        logs = db.query(AuditLog).filter_by(username=username).order_by(
            AuditLog.timestamp.desc()
        ).limit(10).all()

        return [
            {
                "action": log.action,
                "detail": log.detail,
                "timestamp": log.timestamp
            }
            for log in logs
        ]
