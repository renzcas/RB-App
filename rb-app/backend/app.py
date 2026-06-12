from fastapi import FastAPI
from api.routes import bug_bounty, progress, dashboard

app = FastAPI()

app.include_router(bug_bounty.router, prefix="/bug-bounty")
app.include_router(progress.router, prefix="/progress")
app.include_router(dashboard.router, prefix="/dashboard")
