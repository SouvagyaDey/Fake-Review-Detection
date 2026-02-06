from transformers import AutoTokenizer, AutoModelForSequenceClassification
from core.config import MODEL_PATH, BASE_MODEL, DEVICE

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.config.id2label = {0: "not_spam", 1: "spam"}
model.to(DEVICE)
model.eval()

ID2LABEL = model.config.id2label

