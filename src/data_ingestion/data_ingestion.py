
import os
import pandas as pd

def load_data(s3_path: str, nrows: int = None) -> pd.DataFrame:
    """
    Load a CSV from S3 (or local) into a DataFrame, optionally sampling first nrows.
    """
    df = pd.read_csv(s3_path, nrows=nrows)
    return df

def save_data(df: pd.DataFrame, local_path: str):
    """
    Save DataFrame to a local CSV (creates dirs as needed).
    """
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    df.to_csv(local_path, index=False)