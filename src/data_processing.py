import argparse
import pandas as pd
import glob
import os

def load_data(file_path):
    # TODO: Load data from CSV file

    files = [os.path.join(f".\{file_path}", file) for file in os.listdir(f"{file_path}") if file.startswith("gen_") or file.startswith("load_")]

    files_df = pd.DataFrame()

    for file in files:
        df = pd.read_csv(file, sep=",")
        files_df = pd.concat([files_df, df], ignore_index=True)

    return files_df

# def clean_data(df):
#     # TODO: Handle missing values, outliers, etc.

#     return df_clean

# def preprocess_data(df):
#     # TODO: Generate new features, transform existing features, resampling, etc.

#     return df_processed

# def save_data(df, output_file):
#     # TODO: Save processed data to a CSV file
#     pass

def parse_arguments():
    parser = argparse.ArgumentParser(description='Data processing script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file',
        type=str,
        default='data',
        help='Path to the raw data file to process'
    )
    parser.add_argument(
        '--output_file', 
        type=str, 
        default='data/processed_data.csv', 
        help='Path to save the processed data'
    )
    return parser.parse_args()

def main(input_file, output_file):
    df = load_data(input_file)
    print(df)
    # df_clean = clean_data(df)
    # df_processed = preprocess_data(df_clean)
    # save_data(df_processed, output_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.output_file)