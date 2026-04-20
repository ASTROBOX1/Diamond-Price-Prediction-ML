from fastapi import FastAPI, HTTPException
import os
import sys

# Add src to path to import predictors
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.predict import DiamondPricePredictor
from app.schemas import DiamondRequest, PricePrediction

app = FastAPI(
    title="Diamond Price Prediction API",
    description="Professional ML system for estimating diamond prices based on measurements and quality grades.",
    version="1.0.0"
)

# Initialize predictor lazily or at startup
predictor = None

@app.on_event("startup")
def load_model():
    global predictor
    try:
        predictor = DiamondPricePredictor()
    except Exception as e:
        print(f"Error loading model: {e}. API will return 503 until model is trained.")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Diamond Price Prediction API is active."}

@app.post("/predict", response_model=PricePrediction)
def predict_price(diamond: DiamondRequest):
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not initialized. Please run the training pipeline.")
    
    try:
        price = predictor.predict(diamond.dict())
        return PricePrediction(predicted_price=round(price, 2))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health_check():
    if predictor:
        return {"status": "healthy", "model_loaded": True}
    return {"status": "unhealthy", "model_loaded": False}
