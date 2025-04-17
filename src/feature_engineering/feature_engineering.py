
import os
import pandas as pd
from sklearn.model_selection import train_test_split

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode categoricals, drop unused cols, etc.
    """
    df = df.copy()
    # drop id, flight_time if you like:
    df.drop(columns=['id','filght_time'], errors='ignore', inplace=True)

    cat_cols = ['Airline','AirportFrom','AirportTo']
    for col in cat_cols:
        df[col + '_enc'] = df[col].astype('category').cat.codes
    df.drop(columns=cat_cols, inplace=True)

    return df

def split_and_save_data(df: pd.DataFrame, label: str, output_dir: str, test_size=0.2, random_state=42):
    """
    Split df into train/test, save to CSV under output_dir/train-*.csv & test-*.csv.
    """
    os.makedirs(output_dir, exist_ok=True)
    X = df.drop(columns=[label])
    y = df[label]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    train_df = pd.concat([y_train, X_train], axis=1)
    test_df  = pd.concat([y_test,  X_test ], axis=1)

    train_path = os.path.join(output_dir, 'train.csv')
    test_path  = os.path.join(output_dir, 'test.csv')
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path,  index=False)

    return train_path, test_path