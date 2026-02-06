import torch
from core.model import model, tokenizer, ID2LABEL
from core.config import DEVICE

def predict_text(text: str):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)

    conf, label_id = torch.max(probs, dim=1)
    return label_id.item(), conf.item()

def explain_text(text, top_k=5):
    base_label, base_conf = predict_text(text)
    words = text.split()
    impacts = []

    for i, word in enumerate(words):
        masked = words[:i] + words[i+1:]
        if not masked:
            continue

        _, masked_conf = predict_text(" ".join(masked))
        impacts.append((word, base_conf - masked_conf))

    impacts.sort(key=lambda x: x[1], reverse=True)
    important = [w for w, _ in impacts[:top_k]]

    return base_label, base_conf, important

def moderation_action(label: str, confidence: float):
    if label == "spam":
        if confidence > 0.8:
            return "BLOCK"
        elif confidence >= 0.5:
            return "MANUAL_REVIEW"
        else:
            return "APPROVE"
    else:
        # not_spam
        return "APPROVE"
