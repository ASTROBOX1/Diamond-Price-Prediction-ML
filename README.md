# 💎 Diamond Price Prediction System

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ASTROBOX1/Diamond-Price-Prediction-ML)

A production-ready machine learning system for estimating diamond prices based on the "4Cs" (Carat, Cut, Color, Clarity) and physical dimensions.

## 🚀 Key Features

- **Modular pipeline**: Dedicated scripts for cleaning, feature engineering, and training.
- **Robust Cleaning**: Automated handling of NaNs, typos (e.g., `Very Geod`), and zero-dimension outliers.
- **High Performance**: Random Forest model with **98.04% R² Accuracy**.
- **REST API**: FastAPI inference server with Pydantic validation.
- **Dockerized**: Ready for production deployment with a single command.

---

## 📁 Project Structure

- `src/`: Core logic (preprocessing, training, inference).
- `app/`: FastAPI application and schemas.
- `models/`: Trained model and encoder artifacts.
- `data/`: Raw and processed dataset storage.
- `configs/`: YAML configuration files.

---

## 🛠 Setup & Installation

### Prerequisites

- Python 3.12+
- Docker (optional)

### Local Setup

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Train the model**:

   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)/src
   python3 src/train.py
   ```

3. **Run the API server**:

   ```bash
   uvicorn app.main:app --reload
   ```

   Visit `http://localhost:8000/docs` to access the interactive API documentation.

---

## 🐳 Docker Deployment

Build and run the system as a containerized service:

```bash
docker build -t diamond-predictor .
docker run -p 8000:8000 diamond-predictor
```

---

## 📊 API Endpoints

- `GET /`: API Health Check.
- `POST /predict`: Predict diamond price.
  - **Input**: Carat, Cut, Color, Clarity, depth, table, x, y, z.
  - **Output**: Predicted price (USD) and validation metadata.

---

## 🧪 Testing

Run project tests using `pytest`:

```bash
pytest tests/
```
