import pandas as pd
import argparse
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, recall_score, f1_score
from joblib import dump


def load_data(file_path):
    # TODO: Load processed data from CSV file
    df = pd.read_csv(file_path)
    return df

def split_data(df: pd.DataFrame):
    # TODO: Split data into training and validation sets (the test set is already provided in data/test_data.csv)
    x = df.drop('y', axis=1)
    y = df['y']
    X_train, X_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)
    return X_train, X_val, y_train, y_val

def train_model(X_train, y_train, X_val, y_val):
    # TODO: Initialize your model and train it
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)

    # Evaluate model performance
    precision = precision_score(y_val, y_pred, average=None)
    recall = recall_score(y_val, y_pred, average=None)
    f1 = f1_score(y_val, y_pred, average=None)

    precision_micro = precision_score(y_val, y_pred, average='micro')
    recall_micro = recall_score(y_val, y_pred, average='micro')
    f1_micro = f1_score(y_val, y_pred, average='micro')
    
    # Print evaluation metrics
    print("Precision per class:", precision)
    print("Recall per class:", recall)
    print("F1-score per class:", f1)
    print("Precision micro:", precision_micro)
    print("Recall micro:", recall_micro)
    print("F1-score micro:", f1_micro)
    return model

def save_model(model: DecisionTreeClassifier, model_path):
    # TODO: Save your trained model
    dump(model, model_path)
    return

def parse_arguments():
    parser = argparse.ArgumentParser(description='Model training script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file', 
        type=str, 
        default='data/processed_data_train.csv', 
        help='Path to the processed data file to train the model'
    )
    parser.add_argument(
        '--model_file', 
        type=str, 
        default='models/model.pkl', 
        help='Path to save the trained model'
    )
    return parser.parse_args()

def main(input_file, model_file):
    df = load_data(input_file)
    X_train, X_val, y_train, y_val = split_data(df)
    model = train_model(X_train, y_train, X_val, y_val)
    save_model(model, model_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.model_file)