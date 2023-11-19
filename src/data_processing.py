import argparse
import pandas as pd
import glob
import os

def load_data(file_path):
    # TODO: Load data from CSV file
    
    files = [os.path.join(f"./{file_path}", file) for file in os.listdir(f"{file_path}") if file.startswith("gen_") or file.startswith("load_")]

    files_df = pd.DataFrame()

    for file in files:
        df = pd.read_csv(file, sep=",")
        files_df = pd.concat([files_df, df], ignore_index=True)

    return files_df

def clean_data(df: pd.DataFrame):

    # Cambiar el formato de las columnas de tiempo y agruparlas por hora
    df["StartTime"] = pd.to_datetime(df["StartTime"], format="%Y-%m-%dT%H:%M%zZ")
    df["EndTime"] = pd.to_datetime(df["EndTime"], format="%Y-%m-%dT%H:%M%zZ")

    df["StartDayHour"] = df['StartTime'].dt.strftime('%Y-%m-%d %H')
    print(df)
    # df.sort_values(by=['StartTime'], inplace=True)
    # Crear una máscara que sea True cuando load sea nan
    mask = df['Load'].isna()
    
    # Interpolar solo las filas que coincidan con la máscara
    df['quantity'] = df['quantity'].where(mask).interpolate(method='linear')
    df['quantity'].replace(0, None, inplace=True)

    # Filtrar por los tipos de energía verde
    df = df[df['PsrType'].isin(["B01", "B09", "B10", "B11", "B12","B13", "B15", "B16", "B18", "B19", 0])]

    # # Agrupar los datos por AreaID, Load, PsrType y quantity, y sumar los valores numéricos
    # df = df.groupby(['AreaID', 'Load', 'PsrType', 'quantity']).sum().reset_index()

    # Añadir la columna StartTime al resultado, redondeada a la hora más cercana
    df['StartTime'] = df['StartTime'].dt.floor('H')


    # # Añadir una columna que sea la etiqueta
    # def get_label(row):
    #     # Obtener el país con el mayor valor de quantity en la siguiente hora
    #     next_hour = row['StartTime'] + pd.Timedelta(hours=1)
    #     next_row = df[df['StartTime'] == next_hour]
    #     if next_row.empty:
    #         return None # No hay datos para la siguiente hora
    #     else:
    #         max_country = next_row['AreaID'][next_row['quantity'].idxmax()]
    #         return max_country

    # df['label'] = df.apply(get_label, axis=1)
    # print(df)

    # # Asegurarse de que todos los valores estén en las mismas unidades (MAW)
    # df['quantity'] = df['quantity'].astype('float64')
    # print(df)

    df_clean = df
    print(df_clean)
    return df_clean


# def preprocess_data(df):
#     # TODO: Generate new features, transform existing features, resampling, etc.

#     return df_processed

def save_data(df: pd.DataFrame, output_file):
    # TODO: Save processed data to a CSV file
    # Ordenar el dataframe por la fecha de creación
    df = df.sort_values(by='creation_date')

    # Calcular el 80% del número de filas
    n_rows = len(df)
    n_train = int(n_rows * 0.8)

    # Dividir el dataframe en train y test
    df_train = df.iloc[:n_train]
    df_test = df.iloc[n_train:]

    # Guardar los dataframes en archivos CSV
    df_train.to_csv(output_file + '_train.csv', index=False)
    df_test.to_csv(output_file + '_test.csv', index=False)
    return

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
    df_clean = clean_data(df)
    print(df_clean)
    # df_processed = preprocess_data(df_clean)
    save_data(df_clean, output_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.output_file)