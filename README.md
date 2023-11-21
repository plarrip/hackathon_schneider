
# SE-Europe-Data_Challenge_Hackathon_Schneider



## Predicting green energies generation in Europe with ENTSOE data.

In this project, we participate in Schneider Electric's renewable energy prediction challenge, which consists of predicting which country in Europe will generate the most renewable energy in the next hour, using data from the ENTSOE (European Network of Transmission System Operators for Electricity) API. The API provides real-time and historical data on the generation and consumption of different types of energy in European countries. Our goal is to develop a machine learning model that can leverage this data to make accurate and reliable predictions. Those countries and their respective IDs are:

```json
{
    "SP": 0, #Spain
    "UK": 1, #United Kingdom
    "DE": 2, #Germany
    "DK": 3, #Denmark
    "HU": 5, #Hungary
    "SE": 4, #Sweden
    "IT": 6, #Italy
    "PO": 7, #Poland
    "NL": 8  #Netherlands
}
```

This project aims to predict which country will generate the most renewable energy in the next hour, using data from [ENTSOE API](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_psrtype) and machine learning techniques. In this case we used a date range from 2022/01/01 to 2023/01/01. We splitted the data, 80% of the total to train and the rest to test.

### DATA FOLDER

The data folder contains the following files:

- `area_id.json`: A JSON file that maps the area ID to the country name and code.
- `country_id.json`: A JSON file that maps the country ID to the country name and code.
- `load_CI.csv`: A CSV file that contains the raw data from the sources, with the generated energy.
- `gen_CI.csv`: A CSV file that contains the raw data from the sources, with the consumed energy.
- `processed_data_test.csv`: A CSV file that contains the processed data for testing the model.
- `processed_data_train.csv`: A CSV file that contains the processed data for training the model.
- `processed_data_full.csv`: A CSV file that contains the processed data for training and testing the model, with the following columns:
  - `StartTime`: The start time of the hour in UTC.
  - `DE_B01-UK_B19`: The generation of different types of energy in MW for each country.
  - `DE_load-UK_load`: The total load of each country in MW.
  - `DE_surplus-UK_surplus`: The surplus or deficit of each country in MW.
  - `y`: The target variable, which is the country ID that generates the most renewable energy in the next hour.
  - `year`, `month`, `day`, `hour`, `minute`, `second`: The date and time features extracted from the `StartTime` column.

### MODEL FOLDER

The model folder contains the following files:

- `example_model.pkl`: A pickle file that contains an example model trained with a decision tree classifier.
- `model.pkl`: A pickle file that contains the model that we used for the project, trained with the data from ENTSOE API.
- NOTE: We used [sklearn](http://scikit-learn.org) as our maching learning model for this project.


#### MODEL EVALUATION

- `F1-score macro`: 0.9714693295292439
- `Precision macro`: 0.9714693295292439
- `Recall micro`: 0.9714693295292439

### PREDICTIONS FOLDER

The predictions folder contains the following files:

- `example_predictions.json`: A JSON file that contains the example predictions made by the example model, with the following format:

```json
{
    "0": 1,
    "1": 2,
    "2": 3,
    ...
}
```

Where the key is the index of the instance and the value is the country ID predicted for the next hour.

- `predictions.json`: A JSON file that contains the predictions made by our model, with the same format as the example predictions.

### SCRIPTS

The scripts folder is empty, as we did not use any scripts for this project.

### SCR FOLDER

The src folder contains the following Python files:

- `utils.py`: A file that contains some utility functions for the project, we actually didnt touch it I think.
- `data_ingestion.py`: A file that contains the function to load the data from the ENTSOE API, using utils, argparse and datetime libraries.
- `data_processing.py`: A file that contains the function to process the data for training and testing the model, using argparse, pandas, os and json libraries.
- `model_training.py`: A file that contains the function to train the model with the processed data, using sklearn, pandas, argparse and joblib libraries.
- `model_prediction.py`: A file that contains the function to make predictions with the model and the test data, using sklearn, pandas, json, argparse and joblib libraries.
- `csv_to_json.py`: A file that contains the function to convert the CSV file to a JSON file, using argparse and datetime.

### Requirements

The requirements.txt file contains the list of libraries and packages that are needed to run the project, with their respective versions. To install them, you can use the following command:

```bash
pip install -r requirements.txt
```

### How to run the project

To run the project, you need to follow these steps:

1. Clone or download the project repository from GitHub.
2. Install the requirements using the command above.
3. Run the Python files in the src folder in the following order:
   - `data_ingestion.py`
   - `data_processing.py`
   - `model_training.py`
   - `model_prediction.py`
4. Check the output files in the model and predictions folders.

### Contact

If you have any questions or feedback about the project, please contact us. Thank you for your interest in the project. 😊

## Authors

 - [plarrip](https://github.com/plarrip)
 - [gperezz11](https://github.com/gperezz11)
 - [Mar3eczek17](https://github.com/Mar3eczek17)



