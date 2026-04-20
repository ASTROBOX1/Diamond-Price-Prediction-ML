import pandas as pd
import yaml
import logging
import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np

from data_preprocessing import clean_data
from feature_engineering import get_encoders, transform_data, save_encoders

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_path="configs/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def run_training():
    config = load_config()
    
    # 1. Load Data
    logger.info(f"Loading data from {config['data']['raw_path']}")
    df = pd.read_csv(config['data']['raw_path'])
    
    # 2. Preprocessing
    df = clean_data(df)
    
    # 3. Feature Engineering
    logger.info("Starting feature engineering...")
    encoders = get_encoders(config)
    df = transform_data(df, encoders)
    
    # Save encoders for inference
    save_encoders(encoders)
    
    # 4. Split Data
    X = df[config['features']['numerical'] + config['features']['categorical']]
    y = df[config['features']['target']]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=config['model']['params']['random_state']
    )
    
    # 5. Train Model
    logger.info("Training RandomForestRegressor...")
    model = RandomForestRegressor(
        n_estimators=config['model']['params']['n_estimators'],
        random_state=config['model']['params']['random_state']
    )
    model.fit(X_train, y_train)
    
    # 6. Evaluation
    predictions = model.predict(X_test)
    r2 = r2_score(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    
    logger.info(f"Training completed. Metrics: R2 Score = {r2:.4f}, RMSE = {rmse:.4f}")
    
    # 7. Save Model
    os.makedirs(os.path.dirname(config['model']['path']), exist_ok=True)
    joblib.dump(model, config['model']['path'], compress=9)
    logger.info(f"Model saved to {config['model']['path']}")

if __name__ == "__main__":
    run_training()
