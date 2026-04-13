from pydantic import BaseModel, Field

class DiamondRequest(BaseModel):
    carat: float = Field(..., gt=0, example=0.23)
    cut: str = Field(..., example="Ideal")
    color: str = Field(..., example="E")
    clarity: str = Field(..., example="SI2")
    depth: float = Field(..., gt=0, example=61.5)
    table: float = Field(..., gt=0, example=55.0)
    x: float = Field(..., gt=0, example=3.95)
    y: float = Field(..., gt=0, example=3.98)
    z: float = Field(..., gt=0, example=2.43)

class PricePrediction(BaseModel):
    predicted_price: float
    currency: str = "USD"
