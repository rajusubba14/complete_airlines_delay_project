
import os
import pandas as pd

def download_sample_from_s3(s3_path: str, nrows: int, local_dir: str, local_filename: str):
    """
    Downloads the first `nrows` rows of a CSV file from S3 and saves them locally.
    
    Parameters:
    - s3_path: The S3 URL of the CSV file (e.g., "s3://mlprojects-raju/airlinesdelay/Airlines.csv").
    - nrows: Number of rows to read (sample size).
    - local_dir: The local directory where you want to save the file.
    - local_filename: The name for the local CSV file.
    
    Returns:
    - The path to the locally saved sample CSV file.
    """
    # Ensure the local directory exists
    os.makedirs(local_dir, exist_ok=True)
    
    # Construct the full local file path
    local_file = os.path.join(local_dir, local_filename)
    
    # Read only the first `nrows` rows from the CSV file on S3
    print(f"Reading the first {nrows} rows from {s3_path} ...")
    df_sample = pd.read_csv(s3_path, nrows=nrows)
    print(f"Sampled data shape: {df_sample.shape}")
    
    # Save the sampled DataFrame locally
    df_sample.to_csv(local_file, index=False)
    print(f"Sample saved to {local_file}")
    
    return local_file

if __name__ == "__main__":
    # Define parameters
    s3_file = "s3://mlprojects-raju/airlinesdelay/Airlines.csv"
    num_rows = 20000
    destination_dir = os.path.join("data", "raw")
    destination_file = "Airlines_sample.csv"
    
    # Download a sample of the data from S3 and store it locally
    download_sample_from_s3(s3_file, num_rows, destination_dir, destination_file)