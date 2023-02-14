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
rem_list = ['type']

pics = []
for workout in logdata:
    if 'photos' in workout.keys():
        ts = workout.get('timestamp_ms')
        dt = arrow.Arrow.fromtimestamp(ts)
        # Asumi's default timezone for Denver
        if 'Angela Suguro' in workout.get('sender_name'):
            workout['datetime'] = dt.to('US/Central').format('MM-DD-YYYY HH:mm:ss')
            workout['w_date'] = dt.to('US/Central').format('MM-DD-YYYY')
            workout['timestamp'] = dt.to('US/Central').format('HH:mm:ss')
        # Tina's default timezone for NY
        elif 'Tina Peng' in workout.get('sender_name'):
            workout['datetime'] = dt.to('US/Eastern').format('MM-DD-YYYY HH:mm:ss')
            workout['w_date'] = dt.to('US/Eastern').format('MM-DD-YYYY')
            workout['timestamp'] = dt.to('US/Eastern').format('HH:mm:ss')
        else:
            workout['datetime'] = dt.to('US/Pacific').format('MM-DD-YYYY HH:mm:ss')
            workout['w_date'] = dt.to('US/Pacific').format('MM-DD-YYYY')
            workout['timestamp'] = dt.to('US/Pacific').format('HH:mm:ss')
        pics.append(workout)
        #[workout.pop(key) for key in rem_list]

# writes to csv file
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
df = pd.read_csv('workout_data.csv', parse_dates=['datetime','w_date'])

# delete unnecessary columns
df = df.drop(['photos', 'reactions', 'timestamp_ms'], axis=1)

# starting date of workout
first_date = '02/05/2023'
df['startdate'] = pd.to_datetime(first_date, format="%m/%d/%Y")

df['weeknumber'] =  (((df['w_date'] - df['startdate']).dt.days)/7)+1
df['weeknumber'] =  df['weeknumber'].astype(int)
upl_date = datetime.datetime.now()
df['upload_date'] = pd.to_datetime(upl_date)

df.loc[df['weeknumber'] == 1, 'week_goal'] = 2
df.loc[df['weeknumber'] > 1, 'week_goal'] = 3

df['workout_count'] = 1

df=df.sort_values(by='datetime')

# time-series bins
df.loc[df['timestamp'].between('00:00:00','08:00:00'), 'time_type'] = 'early morning'
df.loc[df['timestamp'].between('08:00:00','12:00:00'), 'time_type'] = 'late morning'
df.loc[df['timestamp'].between('12:00:00','17:00:00'), 'time_type'] = 'afternoon'
df.loc[df['timestamp'].between('17:00:00','11:59:59'), 'time_type'] = 'evening'

print(df)

# load data to googlesheet

# function to find next empty row for insertion
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

# credential var
gc = gspread.service_account(filename=r'jsonFileFromGoogle.json')
gkey = '1Utqjn3OIy-5UB3cZtK3DAyqVYkCFQ17VqUwrte1aqm0'
sh = gc.open_by_key(gkey)
worksheet = sh.worksheet("summer23")
next_row = next_available_row(worksheet)

i = int(next_row)
set_with_dataframe(worksheet, df,i,1,False,False,False)