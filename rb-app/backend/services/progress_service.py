from sqlalchemy.orm import Session
from core.database.models import Progress

class ProgressService:
    def mark_completed(self, db: Session, username: str, item_type: str, item_id: str):
        entry = db.query(Progress).filter_by(
            username=username,
            item_type=item_type,
            item_id=item_id
        ).first()

        if not entry:
            entry = Progress(
                username=username,
                item_type=item_type,
                item_id=item_id,
                completed=True
            )
            db.add(entry)
        else:
            entry.completed = True

        db.commit()
        return entry

    def get_user_progress(self, db: Session, username: str):
        return db.query(Progress).filter_by(username=username).all()
