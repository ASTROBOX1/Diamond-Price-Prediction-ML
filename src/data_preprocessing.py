import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the diamonds dataset by dropping duplicates and removing 
    invalid rows with zero values in dimensions (x, y, z).
    """
    initial_shape = df.shape
    logger.info(f"Initial dataset shape: {initial_shape}")

    # Drop duplicates
    df = df.drop_duplicates()
    logger.info(f"Dropped {initial_shape[0] - df.shape[0]} duplicates.")

    # Drop NaNs
    nan_count = df.isna().any(axis=1).sum()
    if nan_count > 0:
        df = df.dropna()
        logger.info(f"Dropped {nan_count} rows containing NaNs.")

    # Correct typos
    typos = {"Very Geod": "Very Good"}
    for typo, correction in typos.items():
        count = len(df[df['cut'] == typo])
        if count > 0:
            df['cut'] = df['cut'].replace(typo, correction)
            logger.info(f"Fixed {count} typos in 'cut' column: {typo} -> {correction}")

    # Drop zero values in x, y, z as per notebook analysis
    # These represent invalid measurements for a diamond
    df = df[(df[['x', 'y', 'z']] != 0).all(axis=1)]
    logger.info(f"Rows after removing zero dimensions: {df.shape[0]}")

    return df

if __name__ == "__main__":
    # Test cleaning logic
    try:
        data = pd.read_csv("data/raw/symbols.csv") # I noted I renamed it to diamonds.csv in task.md but I used mv DiamondData.csv data/raw/diamonds.csv
        # Let's check the path in config or just use hardcoded for local test
        data = pd.read_csv("data/raw/diamonds.csv")
        cleaned_data = clean_data(data)
        print("Cleaning successful.")
    except Exception as e:
        logger.error(f"Cleaning failed: {e}")
