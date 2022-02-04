#TODO: Add a column for week, append out to either csv or googlesheet

import json
import csv
import datetime
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import gspread
from oauth2client.service_account import ServiceAccountCredentials

with open('message_1.json') as json_file:
    data = json.load(json_file)

logdata = data["messages"]

#TODO: use list comprehension
pics = []
for workout in logdata:
    if 'photos' in workout.keys():
        pics.append(workout)

#writes to csv file
data_file = open('workout_data.csv', 'w') 

csv_writer = csv.writer(data_file) 

count = 0

for workout in pics:
    if count == 0:

            header = workout.keys()
            csv_writer.writerow(header)
            count += 1
        
    csv_writer.writerow(workout.values())
data_file.close()

# converting csv file to panda dataframe
df = pd.read_csv('workout_data.csv')

# converts the timestamp to datetime format
df['timestamp_ms'] = pd.to_datetime(df.timestamp_ms, unit='ms')
df['timestamp_ms'] = pd.to_datetime(df.timestamp_ms, format='%Y%m%d')

# delete unnecessary columns
df = df.drop(['photos', 'reactions', 'type', 'is_unsent'], axis=1)
print(df)


#load data to googlesheet
#gc = gspread.service_account(filename=r'C:\Users\chris\workout\jsonFileFromGoogle.json')

#sh = gc.open_by_key('1Utqjn3OIy-5UB3cZtK3DAyqVYkCFQ17VqUwrte1aqm0')

#worksheet = sh.worksheet("Log2")

#set_with_dataframe(worksheet, df)