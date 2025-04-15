from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score
import sklearn
import joblib
import boto3
import pathlib
from io import StringIO
import argparse
import os
import pandas as pd
import numpy as np

def model_fn(model_dir):
    # Correctly join the path and load the model.
    clf = joblib.load(os.path.join(model_dir, "model.joblib"))
    return clf

if __name__ == "__main__":
    print("[INFO] Extracting arguments")
    parser = argparse.ArgumentParser()
    
    # Hyperparameters sent as command line arguments
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--random_state", type=int, default=0)

    # Data directories and file names
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR", "./model"))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN", "."))
    parser.add_argument("--test", type=str, default=os.environ.get("SM_CHANNEL_TEST", "."))
    parser.add_argument("--train-file", type=str, default="train-v-1.csv")
    parser.add_argument("--test-file", type=str, default="test-v-1.csv")

    args, _ = parser.parse_known_args()
    
    print("SKlearn Version: ", sklearn.__version__)
    print("Joblib Version: ", joblib.__version__)
    
    print("[INFO] Reading data")
    
    train_df = pd.read_csv(os.path.join(args.train, args.train_file))
    test_df = pd.read_csv(os.path.join(args.test, args.test_file))
    
    features = list(train_df.columns)
    label = features.pop(-1)
    
    print("Building training and testing datasets")
    print("Column order: ")
    print(features)
    print("Label column is: ", label)
    
    print("Data Shape: ")
    print("------- SHAPE OF TRAINING DATA -------")
    print(train_df[features].shape, train_df[label].shape)
    print("------- SHAPE OF TESTING DATA -------")
    print(test_df[features].shape, test_df[label].shape)
    
    print("Training RandomForest Model ...")
    model = RandomForestClassifier(n_estimators=args.n_estimators, random_state=args.random_state)
    model.fit(train_df[features], train_df[label])
    
    # Ensure the model directory exists before saving the model
    if not os.path.exists(args.model_dir):
        os.makedirs(args.model_dir, exist_ok=True)
        
    model_path = os.path.join(args.model_dir, "model.joblib")
    joblib.dump(model, model_path)
    print("Model saved at: " + model_path)
    
    y_pred_test = model.predict(test_df[features])
    test_acc = accuracy_score(test_df[label], y_pred_test)
    test_rep = classification_report(test_df[label], y_pred_test)
    
    print("---- METRICS RESULTS FOR TESTING DATA ----")
    print("Total Rows:", test_df.shape[0])
    print("[TESTING] Model Accuracy:", test_acc)
    print("[TESTING] Testing Report:")
    print(test_rep)
