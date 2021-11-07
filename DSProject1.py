# -*- coding: utf-8 -*-

# -- Sheet --

import requests
import pandas as pd
import json
import sys
import os.path


# normals daily: https://www.ncdc.noaa.gov/cdo-web/datasets

"Fetch / download / retrieve a remote data file by URL"
# getting csv from url
csv_url="https://www1.ncdc.noaa.gov/pub/data/cdo/samples/NORMAL_DLY_sample_csv.csv"
r = requests.get(csv_url)
# informative error for request operation
r.raise_for_status()
# continues if request successful
url_content = r.content
# writing content to csv file
csv_file = open('normaldata.csv', 'wb')
csv_file.write(url_content)
csv_file.close()


#reading in newly written csv and informative error if csv file path incorrect
path = 'normaldata.csv'
file_exists = os.path.exists(path)
if file_exists:
    # if it works, print first 5 rows of csv file
    df = pd.read_csv(path)
    print(df.head())
else:
    sys.exit('The file path for the csv was: ' + path + '. This path resulted in a file not found error.')

"Generate brief summary of data file:"
record_count = len(df)
column_count = len(df.columns)
print("Column count: " + str(column_count))
print("Record count: " + str(record_count))
"So, there are 9 columns and 365 records"


"Modify number of columns from source to destination by reducing columns"
# dropping station name b/c only one unique value for both columns
# print(df['STATION_NAME'].unique())
# including informative error if column name not found
dropped_column = 'STATION_NAME'
found = df.get(dropped_column)
if found.empty:
    sys.exit("The column to be dropped, " + dropped_column + ", was not found.")
else:
    df.drop(dropped_column, inplace=True, axis=1)

"Convert to json and Write to disk"
df = df.to_json('normaldata.json')


# checking json file written to disk correctly, if not, producing informative error
with open('normaldata.json','r') as json_file:
    loaded_json = json.load(json_file)
    key_count = 0
    for key,value in loaded_json.items():
        print(key)
        key_count += 1
    if key_count != 8:
        print("Expected json file to have 8 columns written to it, instead " + str(key_count) + " columns written.")
    json_file.close()
