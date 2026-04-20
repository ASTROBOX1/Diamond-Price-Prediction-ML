import joblib
import pandas as pd
import yaml
import os

class DiamondPricePredictor:
    def __init__(self, model_path="models/model.joblib", encoder_path="models/encoders.joblib"):
        # Use absolute paths relative to this file for better portability
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        model_path = os.path.join(base_dir, model_path)
        encoder_path = os.path.join(base_dir, encoder_path)
        config_path = os.path.join(base_dir, "configs/config.yaml")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}. Please run training first.")
        if not os.path.exists(encoder_path):
            raise FileNotFoundError(f"Encoder file not found at {encoder_path}. Please run training first.")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found at {config_path}.")
        
        self.model = joblib.load(model_path)
        self.encoders = joblib.load(encoder_path)
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def predict(self, input_data: dict) -> float:
        """
        Predicts the price of a diamond based on input features.
        input_data: dictionary containing carat, cut, color, clarity, depth, table, x, y, z
        Raises: ValueError if inputs are invalid
        """
        # Validate required fields
        required_fields = ['carat', 'cut', 'color', 'clarity', 'depth', 'table', 'x', 'y', 'z']
        missing_fields = [f for f in required_fields if f not in input_data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        # Validate numeric ranges
        if input_data.get('carat', 0) <= 0:
            raise ValueError("Carat must be positive")
        if input_data.get('x', 0) <= 0 or input_data.get('y', 0) <= 0 or input_data.get('z', 0) <= 0:
            raise ValueError("Dimensions (x, y, z) must be positive")
        
        df = pd.DataFrame([input_data])
        
        # Apply the same categorical transformation used in training (using transform only, not fit_transform)
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
