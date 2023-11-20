import argparse
import pandas as pd
import glob
import os
from datetime import datetime
import pandas as pd
import json

def load_data(file_path):
    # TODO: Load data from CSV file
    
    files = [os.path.join(f"./{file_path}", file) for file in os.listdir(f"{file_path}") if file.startswith("gen_") or file.startswith("load_")]

    gen_dfs = []
    load_dfs = []

    for file in files:
        df = pd.read_csv(file, sep=",")
        
        # Extracting country and eType from the filename
        country = os.path.splitext(os.path.basename(file))[0].split('_')[1]
        
        # Adding 'Country' columns to the DataFrame
        df['Country'] = country

        # Separating DataFrames based on the file prefix
        if "gen_" in file:
            gen_dfs.append(df)
        elif "load_" in file:
            load_dfs.append(df)

    return gen_dfs, load_dfs



def clean_data(gen_dfs, load_dfs):
    # TODO: Handle missing values, outliers, etc.

    #process Gen dataframes
    df1 = pd.DataFrame()
    duplicated=0
    nans=0
    for df in gen_dfs:
        #dropping 'AreaID' and 'UnitName' columns that are useless
        df.drop(columns=['AreaID','UnitName'], inplace=True)

        #checking duplicated rows
        duplicated = duplicated + df.duplicated().sum()
        if df.duplicated().sum() > 0:
            duplicated_rows = df.duplicated()
            df = df[~duplicated_rows]
        #checking rows with NaN
        nans = nans + df[df.isna().any(axis=1)].sum()

        #filtering by green energy PsrType
        df = df[df['PsrType'].isin(["B01", "B09", "B10", "B11", "B12","B13", "B15", "B16", "B18", "B19"])]
        if len(df)<1: continue

        #saving for later
        PsrType = df.PsrType[0]
        Country = df.Country[0]

        # Convert to datetime
        df["StartTime"] = pd.to_datetime(df["StartTime"], format="%Y-%m-%dT%H:%M%zZ")
        df["EndTime"] = pd.to_datetime(df["EndTime"], format="%Y-%m-%dT%H:%M%zZ")
        # Set the index to 'StartTime'
        df.set_index('StartTime', inplace=True)
        df = df.resample('H').sum()
        #renaming the quantity column for later (replaces the pivoting)
        df.rename(columns={'quantity':Country+'_'+PsrType}, inplace=True)
        df.reset_index(inplace=True)

        #merge with the rest of DFs
        if len(df1) == 0:
            df1 = df.copy()
        else:
            df1 = pd.merge(df1, df, on='StartTime', how='outer')

    print("Total duplicated rows: ", duplicated)
    print("Total NaN rows: ", nans)

    #process Load dataframes
    df2 = pd.DataFrame()
    duplicated=0
    nans=0
    for df in load_dfs:
        #dropping 'AreaID' and 'UnitName' columns that are useless
        df.drop(columns=['AreaID','UnitName'], inplace=True)

        #checking duplicated rows
        duplicated = duplicated + df.duplicated().sum()
        if df.duplicated().sum() > 0:
            duplicated_rows = df.duplicated()
            df = df[~duplicated_rows]
        #checking rows with NaN
        nans = nans + df[df.isna().any(axis=1)].sum()

        #saving for later
        Country = df.Country[0]

        # Convert to datetime
        df["StartTime"] = pd.to_datetime(df["StartTime"], format="%Y-%m-%dT%H:%M%zZ")
        df["EndTime"] = pd.to_datetime(df["EndTime"], format="%Y-%m-%dT%H:%M%zZ")
        # Set the index to 'StartTime'
        df.set_index('StartTime', inplace=True)
        df = df.resample('H').sum()
        #renaming the quantity column for later (replaces the pivoting)
        df.rename(columns={'Load':Country+'_load'}, inplace=True)
        df.reset_index(inplace=True)

        #merge with the rest of DFs
        if len(df2) == 0:
            df2 = df.copy()
        else:
            df2 = pd.merge(df2, df, on='StartTime', how='outer')

    print("Total duplicated rows: ", duplicated)
    print("Total NaN rows: ", nans)

    #MERGE GEN AND LOAD DATAFRAMES
    df_clean = pd.merge(df1, df2, on='StartTime', how='outer')
    return df_clean


def preprocess_data(df3):
    #TODO: Generate new features, transform existing features, resampling, etc.

    df3 = df3[['StartTime'] + sorted([col for col in df3.columns if col not in ['StartTime']])]
    #INTERPOLATE TO GIVE VALUE TO NaN cells
    df3.set_index('StartTime', inplace=True)
    df3.interpolate(method='linear', limit_direction='both', inplace=True)
    #CALCULATING THE SURPLUS COLUMNS
    df4 = df3.copy()
    # Extract unique prefixes (e.g., 'DE', 'DK')
    prefixes = set(col.split('_')[0] for col in df4.columns)

    # Iterate through prefixes and calculate surplus
    for prefix in prefixes:
        # Select columns for the current country and load
        country_cols = [col for col in df4.columns if col.startswith(prefix) and col != f'{prefix}_load']
        
        # Create a new column for surplus
        df4[f'{prefix}_surplus'] = df4[country_cols].sum(axis=1) - df4[f'{prefix}_load']

    #resorting the columns for clarity
    df4 = df4[sorted([col for col in df4.columns if col not in ['StartTime']])]

    #finding the country with the most surplus per hour
    df5 = df4.copy()
    # Filter columns with 'surplus' in the name
    surplus_columns = [col for col in df5.columns if 'surplus' in col]

    # Create a new column with the country code having the highest surplus
    df5['y'] = df5[surplus_columns].idxmax(axis=1).str.split('_').str[0]

    #mapping the country in column 'y' to numeric
    # Load the country list from the JSON file
    with open('./data/country_list.json', 'r') as file:
        country_mapping = json.load(file)

    df5['y'] = df5['y'].map(country_mapping)
    df_processed = df5.copy()

    return df_processed

def save_data(df_processed: pd.DataFrame, output_file):
    # TODO: Save processed data to a CSV file
    # Ordenar el dataframe por la fecha de creación
    df_processed.sort_values(by=['StartTime'], inplace=True)

    # Calcular el 80% del número de filas
    n_rows = len(df_processed)
    n_train = int(n_rows * 0.8)

    # Dividir el dataframe en train y test  
    df_train = df_processed.iloc[:n_train].reset_index()
    df_test = df_processed.iloc[n_train:].reset_index()
    df_full = df_processed.copy().reset_index()

    # Guardar los dataframes en archivos CSV
    df_train.to_csv(output_file + 'train.csv', index=False)
    df_test.to_csv(output_file + 'test.csv', index=False)
    df_full.to_csv(output_file + 'full.csv', index=False)  #file used to explore the dataset graphically. Refer to 'data_exploration.ipynb'.
    pass

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
        default='data/processed_data_', 
        help='Path to save the processed data'
    )
    return parser.parse_args()

def main(input_file, output_file):
    gen_dfs, load_dfs = load_data(input_file)
    df_clean = clean_data(gen_dfs, load_dfs)
    df_processed = preprocess_data(df_clean)
    save_data(df_processed, output_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.output_file)