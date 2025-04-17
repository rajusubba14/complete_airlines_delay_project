from src.data_ingestion.data_ingestion import load_data, save_data
from src.eda.eda import run_eda
from src.feature_engineering.feature_engineering import engineer_features, split_and_save_data
from src.model.model_training import train_model
from src.model.model_evaluation import evaluate_model

def main():
    df = load_data("s3://mlprojects-raju/airlinesdelay/Airlines.csv", nrows=20000)
    save_data(df, "data/raw/sample.csv")
    run_eda(df, "reports/eda")
    fe = engineer_features(df)
    train_csv, test_csv = split_and_save_data(fe, label="Delay", output_dir="data/processed")
    model = train_model(train_csv, model_dir="model")
    evaluate_model(test_csv, "model/model.joblib")

if __name__=="__main__":
    main()