import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
import joblib
import os
import yaml

def load_config():
    with open("configs/config.yaml", "r") as f:
        return yaml.safe_load(f)

def get_encoders(config):
    """
    Creates OrdinalEncoders based on explicit order defined in config.
    """
    encoders = {}
    for col in config['encoding']:
        categories = [config['encoding'][col]]
        encoder = OrdinalEncoder(categories=categories)
        encoders[col] = encoder
    return encoders

def transform_data(df: pd.DataFrame, encoders: dict) -> pd.DataFrame:
    """
    Applies the encoders to the specified columns.
    """
    df_transformed = df.copy()
    for col, enc in encoders.items():
        if col in df_transformed.columns:
            # Reshape to 2D for sklearn transformer
            df_transformed[[col]] = enc.fit_transform(df_transformed[[col]])
    return df_transformed

def save_encoders(encoders, path="models/encoders.joblib"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(encoders, path)

if __name__ == "__main__":
    # Test encoding
    config = load_config()
    test_df = pd.DataFrame({
        'cut': ['Ideal', 'Good'],
        'color': ['E', 'J'],
        'clarity': ['VS1', 'I1']
    })
    encoders = get_encoders(config)
    transformed = transform_data(test_df, encoders)
    print(transformed)
