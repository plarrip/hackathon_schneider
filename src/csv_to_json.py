import csv
import json

# Assuming your CSV file has two columns: 'key' and 'value'
csv_file_path = 'data/AreaID_dict.csv'
json_file_path = 'data/AreaID_dict.json'

# Read data from CSV and convert it to a dictionary
data_dict = {}
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        key = row['Code']
        value = row['Meaning']
        data_dict[key] = value

# Write the dictionary to a JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(data_dict, json_file, indent=2)
