# -*- coding: utf-8 -*-

# -- Sheet --

import requests
import pandas as pd
import json


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


#reading in newly written csv,
df = pd.read_csv ('normaldata.csv')
print(df.head())

"Generate brief summary of data file:"
record_count = len(df)
column_count = len(df.columns)
print("Column count: " + str(column_count))
print("Record count: " + str(record_count))
"So, there are 9 columns and 365 records"


"Modify number of columns from source to destination by reducing columns"
# dropping station name b/c only one unique value for column
# print(df['STATION_NAME'].unique())
df.drop('STATION_NAME', inplace=True, axis=1)

"Convert to json and Write to disk"
df = df.to_json('normaldata.json')


# checking json file written to disk correctly
with open('normaldata.json','r') as json_file:
    loaded_json = json.load(json_file)
    for key,value in loaded_json.items():
        print(key)
    json_file.close()
