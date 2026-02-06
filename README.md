# Fake Review Detection API

A FastAPI-based REST API for detecting fake/spam reviews using a fine-tuned DistilBERT model.

## Features

- **ML-Powered Detection** — Fine-tuned DistilBERT for spam classification
- **API Key Authentication** — Secure endpoints with user API keys
- **Usage Tracking** — Admin dashboard to monitor requests per user
- **Batch Processing** — Analyze multiple reviews in one request
- **Moderation Actions** — Get recommended actions (APPROVE/BLOCK/MANUAL_REVIEW)

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| ML Model | DistilBERT (fine-tuned) |
| Database | SQLite |
| ORM | SQLAlchemy |

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/frdetect.git
cd frdetect

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn torch transformers sqlalchemy pydantic

# Run the server
uvicorn app:app --reload
```

On first startup, an admin API key is printed:
```
Admin user created! API Key: <save_this_key>
```

## Authentication Flow

```
Request → X-API-Key header → Database lookup → User validated → Endpoint runs
```

| Scenario | Response |
|----------|----------|
| No API key | `422 Unprocessable Entity` |
| Invalid key | `401 Unauthorized` |
| Valid key | Success |

---

## API Endpoints

### Health & Info (No Auth)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/model/info` | Model version info |
| `GET` | `/docs` | Swagger UI |

---

### 👤 Users

#### Create User
```http
POST /users
Content-Type: application/json

{
  "username": "myuser"
}
```

**Response:**
```json
{
  "username": "myuser",
  "api_key": "1ec5fa1161f58fc5e62e0ffd9133a811"
}
```

---

### 🔍 Reviews (Requires API Key)

#### Predict Single
```http
POST /reviews/predict
Content-Type: application/json
X-API-Key: YOUR_API_KEY

{
  "review": "This product is amazing!"
}
```

**Response:**
```json
{
  "label": "spam",
  "confidence": 0.9234
}
```

#### Predict Batch
```http
POST /reviews/predict/batch
Content-Type: application/json
X-API-Key: YOUR_API_KEY

{
  "reviews": [
    "Great product!",
    "Terrible quality, broke immediately"
  ]
}
```

**Response:**
```json
{
  "results": [
    {"label": "spam", "confidence": 0.8765},
    {"label": "not spam", "confidence": 0.9123}
  ]
}
```

#### Moderate
```http
POST /reviews/moderate
Content-Type: application/json
X-API-Key: YOUR_API_KEY

{
  "review": "BUY NOW! LIMITED OFFER!!!"
}
```

**Response:**
```json
{
  "label": "spam",
  "confidence": 0.9567,
  "action": "BLOCK"
}
```

---

### 👑 Admin (Requires Admin API Key)

#### Usage by User
```http
GET /admin/usage
X-API-Key: ADMIN_API_KEY
```

**Response:**
```json
[
  {
    "user_id": "1ec5fa...",
    "total_requests": 15,
    "endpoints": {
      "/reviews/predict": 10,
      "/reviews/moderate": 5
    }
  }
]
```

#### Usage Logs (Detailed)
```http
GET /admin/usage/logs
X-API-Key: ADMIN_API_KEY
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": "1ec5fa...",
    "endpoint": "/reviews/predict",
    "minute_bucket": "2026-02-07T10:30:00",
    "request_count": 3
  }
]
```

#### Usage Summary
```http
GET /admin/usage/summary
X-API-Key: ADMIN_API_KEY
```

**Response:**
```json
[
  {"user_id": "1ec5fa...", "total_requests": 15},
  {"user_id": "49d6e4...", "total_requests": 8}
]
```

---

## 📁 Project Structure

```
frdetect/
├── app.py                 # FastAPI app, middleware, startup
├── core/
│   ├── auth.py            # get_current_user, require_admin
│   ├── config.py          # MODEL_PATH, DEVICE
│   ├── database.py        # SQLAlchemy engine
│   ├── model.py           # Load DistilBERT model
│   ├── usage_tracker.py   # APIUsage model
│   └── user.py            # User model
├── routers/
│   ├── admin.py           # /admin/* endpoints
│   ├── reviews.py         # /reviews/* endpoints
│   └── users.py           # /users endpoint
├── schemas/
│   └── review.py          # Pydantic request/response models
├── services/
│   └── inference.py       # predict_text, moderation_action
├── tests/
│   ├── test_auth.py
│   ├── test_moderate.py
│   └── test_predict.py
└── distillbert_results/   # Fine-tuned model checkpoint
```

## Labels

| ID | Label | Description |
|----|-------|-------------|
| 0 | `not spam` | Genuine review |
| 1 | `spam` | Fake/spam review |

## Run Tests

```bash
pytest
```

## 📄 License

MIT
