from sqlalchemy.orm import Session
from core.database.models import AuditLog

def log_action(db: Session, username: str, action: str, detail: str = ""):
    entry = AuditLog(
        username=username,
        action=action,
        detail=detail
    )
    db.add(entry)
    db.commit()
