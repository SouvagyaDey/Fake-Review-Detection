from fastapi import APIRouter, Depends
from schemas.review import (
    TextRequest,
    BatchRequest,
    PredictionResponse,
    ExplainResponse,
    ModerateResponse
)
from services.inference import (
    predict_text,
    explain_text,
    moderation_action
)
from core.model import ID2LABEL
from core.auth import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/predict", response_model=PredictionResponse)
def predict(req: TextRequest, user=Depends(get_current_user)):
    label_id, conf = predict_text(req.review)
    return {"label": ID2LABEL[label_id], "confidence": round(conf, 4)}

@router.post("/predict/batch")
def predict_batch(req: BatchRequest, user=Depends(get_current_user)):
    return {
        "results": [
            {
                "label": ID2LABEL[predict_text(r)[0]],
                "confidence": round(predict_text(r)[1], 4)
            }
            for r in req.reviews
        ]
    }


@router.post("/moderate", response_model=ModerateResponse)
def moderate(req: TextRequest, user=Depends(get_current_user)):
    label_id, conf = predict_text(req.review)
    label = ID2LABEL[label_id]

    action = moderation_action(label, conf)

    return {
        "label": label,
        "confidence": round(conf, 4),
        "action": action
    }

