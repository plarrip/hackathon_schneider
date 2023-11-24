import pandas as pd
import argparse
import json
from sklearn.tree import DecisionTreeClassifier
from joblib import load


def load_data(file_path) -> pd.DataFrame:
    """Load test data from CSV file"""
    # TODO: Load test data from CSV file
    df = pd.read_csv(file_path)
    df = df.drop(columns=['y'])
    return df


def load_model(model_path) -> DecisionTreeClassifier:
    """Load trained model"""
    # TODO: Load the trained model
    model = load(model_path)
    return model


def make_predictions(df, model: DecisionTreeClassifier) -> list[dict[str, int]]:
    """Make predictions on test data"""
    # TODO: Use the model to make predictions on the test data
    predictions = model.predict(df)

    predictions_dict = {
        "target": {
            f"{i}": int(p) for i, p in enumerate(predictions)
        }
    }

    return predictions_dict


def save_predictions(predictions, predictions_file):
    """Save predictions to a JSON file"""
    # TODO: Save predictions to a JSON file
    with open(predictions_file, 'w') as f:
        json.dump(predictions, f)
    return


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Prediction script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file',
        type=str,
        default='data/processed_data_test.csv',
        help='Path to the test data file to make predictions'
    )
    parser.add_argument(
        '--model_file',
        type=str,
        default='models/model.pkl',
        help='Path to the trained model file'
    )
    parser.add_argument(
        '--output_file',
        type=str,
        default='./predictions.json',
        help='Path to save the predictions'
    )
    return parser.parse_args()


def main(input_file, model_file, output_file):
    df = load_data(input_file)
    model = load_model(model_file)
    predictions = make_predictions(df, model)
    save_predictions(predictions, output_file)


if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.model_file, args.output_file)
