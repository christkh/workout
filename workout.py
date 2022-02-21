#TODO: Add a column for week, append out to either csv or googlesheet

import json
import csv
import datetime
import pandas as pd
import arrow
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import gspread

with open('message_1.json') as json_file:
    data = json.load(json_file)

logdata = data["messages"]

#TODO: use list comprehension
pics = []
for workout in logdata:
    if 'photos' in workout.keys():
        ts = workout.get('timestamp_ms')
        dt = arrow.Arrow.fromtimestamp(ts)
        workout['datetime'] = dt.to('US/Pacific').format('MM-DD-YYYY HH:mm:ss')
        workout['w_date'] = dt.to('US/Pacific').format('MM-DD-YYYY')
        pics.append(workout)

print(pics)

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

#converting csv file to panda dataframe
df = pd.read_csv('workout_data.csv', parse_dates=['datetime','w_date'])

#delete unnecessary columns
df = df.drop(['photos', 'reactions', 'type', 'is_unsent', 'timestamp_ms'], axis=1)

#starting date of workout
df['startdate'] = pd.to_datetime('02/14/2022')

df['weeknumber'] =  (((df['w_date'] - df['startdate']).dt.days)/7)+1
df['weeknumber'] =  df['weeknumber'].astype(int)

print(df)

#load data to googlesheet
#gc = gspread.service_account(filename=r'C:\Users\chris\workout\jsonFileFromGoogle.json')

gc = gspread.service_account(filename=r'jsonFileFromGoogle.json')

gkey = '1Utqjn3OIy-5UB3cZtK3DAyqVYkCFQ17VqUwrte1aqm0'
sh = gc.open_by_key(gkey)

worksheet = sh.worksheet("Log")

#i = 1

#while worksheet.cell(i,1).value != "":
#    i = i + 1

set_with_dataframe(worksheet, df)