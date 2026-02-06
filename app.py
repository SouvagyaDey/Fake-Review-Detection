from fastapi import FastAPI, Request
from routers.reviews import router as review_router
from routers.admin import router as admin_router
from routers.users import router as users_router

# DB imports
from core.database import engine
from core.usage_tracker import Base, APIUsage
from core.user import User
from core.database import SessionLocal
from datetime import datetime, timezone
import secrets

app = FastAPI(title="Fake Review Detection API")


Base.metadata.create_all(bind=engine)

# Create default admin user if none exists
def init_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.is_admin == True).first()
    if not admin:
        api_key = secrets.token_hex(16)
        admin = User(username="admin", api_key=api_key, is_admin=True)
        db.add(admin)
        db.commit()
        print(f"Admin user created! API Key: {api_key}")
    db.close()

init_admin()


IGNORED_ENDPOINTS = ["/health", "/model/info", "/docs", "/openapi.json"]

@app.middleware("http")
async def track_api_usage(request: Request, call_next):
    response = await call_next(request)

    path = request.url.path
    if path in IGNORED_ENDPOINTS:
        return response

    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return response

    minute_bucket = datetime.now(timezone.utc).replace(second=0, microsecond=0)

    db = SessionLocal()
    record = db.query(APIUsage).filter_by(
        user_id=api_key,
        endpoint=path,
        minute_bucket=minute_bucket
    ).first()

    if record:
        record.request_count += 1
    else:
        db.add(APIUsage(
            user_id=api_key,
            endpoint=path,
            minute_bucket=minute_bucket,
            request_count=1
        ))

    db.commit()
    db.close()

    return response


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/model/info")
def model_info():
    return {
        "model": "FakeReviewClassifier",
        "version": "1.0.0"
    }

app.include_router(review_router)
app.include_router(admin_router)
app.include_router(users_router)
