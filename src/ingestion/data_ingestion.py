
import os
import pandas as pd
import boto3

def download_and_sample_data(s3_bucket, s3_key, nrows, local_raw_dir, local_filename):
    # S3 path like "s3://mlprojects-raju/airlinesdelay/Airlines.csv"
    s3_path = f"s3://mlprojects-raju/airlinesdelay/Airlines.csv"
    
    print(f"Reading first {nrows} rows from {s3_path}...")
    df = pd.read_csv(s3_path, nrows=nrows)
    print("Data read. Shape:", df.shape)
    
    # Ensure the local directory exists
    os.makedirs(local_raw_dir, exist_ok=True)
    local_file = os.path.join(local_raw_dir, local_filename)
    
    print(f"Saving sampled data to {local_file}...")
    df.to_csv(local_file, index=False)
    
    return local_file

def upload_to_s3(local_file, s3_bucket, s3_key):
    s3 = boto3.client("s3")
    print(f"Uploading {local_file} to s3://{s3_bucket}/{s3_key} ...")
    s3.upload_file(local_file, s3_bucket, s3_key)
    print("Upload complete.")

if __name__ == "__main__":
    # Define S3 bucket and key for the input data.
    s3_bucket = "mlprojects-raju"
    s3_input_key = "airlinesdelay/Airlines.csv"
    
    # Define number of rows to sample
    nrows = 20000
    
    # Define local raw directory and file name to save the sampled data
    local_raw_dir = os.path.join("data", "raw")
    local_filename = "Airlines_sample.csv"
    
    # Download and sample data
    local_file = download_and_sample_data(s3_bucket, s3_input_key, nrows, local_raw_dir, local_filename)
    
    # (Optional) If you want to upload the local file back to S3 in a raw folder:
    s3_output_key = "airlinesdelay/raw/Airlines_sample.csv"
    upload_to_s3(local_file, s3_bucket, s3_output_key)
    
    print("Process complete.")