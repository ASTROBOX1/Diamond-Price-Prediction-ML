import joblib
import pandas as pd
import yaml
import os

class DiamondPricePredictor:
    def __init__(self, model_path="models/model.joblib", encoder_path="models/encoders.joblib"):
        self.model = joblib.load(model_path)
        self.encoders = joblib.load(encoder_path)
        with open("configs/config.yaml", "r") as f:
            self.config = yaml.safe_load(f)

    def predict(self, input_data: dict) -> float:
        """
        Predicts the price of a diamond based on input features.
        input_data: dictionary containing carat, cut, color, clarity, depth, table, x, y, z
        """
        df = pd.DataFrame([input_data])
        
        # Apply the same categorical transformation used in training
        for col, enc in self.encoders.items():
            if col in df.columns:
                df[[col]] = enc.transform(df[[col]])
        
        # Ensure correct feature order
        features = self.config['features']['numerical'] + self.config['features']['categorical']
        df = df[features]
        
        prediction = self.model.predict(df)
        return float(prediction[0])

if __name__ == "__main__":
    # Test prediction (Assumes model exists)
    try:
        predictor = DiamondPricePredictor()
        sample_diamond = {
            "carat": 0.23,
            "cut": "Ideal",
            "color": "E",
            "clarity": "SI2",
            "depth": 61.5,
            "table": 55.0,
            "x": 3.95,
            "y": 3.98,
            "z": 2.43
        }
        price = predictor.predict(sample_diamond)
        print(f"Predicted Price: ${price:.2f}")
    except Exception as e:
        print(f"Prediction failed: {e}. (Run train.py first)")
