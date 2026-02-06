import torch

MODEL_PATH = "distillbert_results/checkpoint-6066"
BASE_MODEL = "distilbert-base-uncased"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"