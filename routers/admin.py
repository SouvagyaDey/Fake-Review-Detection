from fastapi import APIRouter, Depends
from sqlalchemy import func
from core.database import SessionLocal
from core.usage_tracker import APIUsage
from core.auth import get_db, require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/usage")
def get_usage(user_id: str | None = None, admin=Depends(require_admin)):

    db = SessionLocal()
    
    # Get all users or filter by user_id
    if user_id:
        users = [user_id]
    else:
        users = [r[0] for r in db.query(APIUsage.user_id).distinct().all()]
    
    result = []
    for uid in users:
        total = db.query(func.sum(APIUsage.request_count)).filter(
            APIUsage.user_id == uid
        ).scalar() or 0
        
        endpoints = db.query(
            APIUsage.endpoint,
            func.sum(APIUsage.request_count).label("count")
        ).filter(APIUsage.user_id == uid).group_by(APIUsage.endpoint).all()
        
        result.append({
            "user_id": uid,
            "total_requests": total,
            "endpoints": {e.endpoint: e.count for e in endpoints}
        })
    
    db.close()
    return result


@router.get("/usage/logs")
def get_usage_logs(user_id: str | None = None, admin=Depends(require_admin)):
    db = SessionLocal()
    q = db.query(APIUsage)
    if user_id:
        q = q.filter(APIUsage.user_id == user_id)

    rows = q.order_by(APIUsage.minute_bucket.desc()).all()
    db.close()

    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "endpoint": r.endpoint,
            "minute_bucket": r.minute_bucket,
            "request_count": r.request_count
        }
        for r in rows
    ]


@router.get("/usage/summary")
def get_usage_summary(admin=Depends(require_admin), db=Depends(get_db)):

    results = db.query(
        APIUsage.user_id,
        func.sum(APIUsage.request_count).label("total_requests")
    ).group_by(APIUsage.user_id).all()

    return [{"user_id": r.user_id, "total_requests": r.total_requests} for r in results]

