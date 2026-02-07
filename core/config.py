import os
import torch
from dotenv import load_dotenv

load_dotenv()

# From .env
MODEL_REPO = os.getenv("MODEL_REPO", "Souvagya/fake-review-distilbert")
HF_TOKEN = os.getenv("HF_TOKEN")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
