from transformers import AutoTokenizer, AutoModelForSequenceClassification
from core.config import MODEL_REPO, HF_TOKEN, DEVICE

# Tokenizer from base model (always available)
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# Model from your HF repo
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_REPO,
    token=HF_TOKEN
)

if model.config.id2label.get(0, "").startswith("LABEL"):
    model.config.id2label = {
        0: "not_spam",
        1: "spam"
    }

model.to(DEVICE)
model.eval()

ID2LABEL = model.config.id2label
