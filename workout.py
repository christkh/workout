import json
import csv
import datetime
import pandas as pd

with open('message_1.json') as json_file:
    data = json.load(json_file)

workout_data = data['messages']

data_file = open('workout_data.csv', 'w') 

csv_writer = csv.writer(data_file) 

count = 0

for workout in workout_data:
    if count == 0:

            header = workout.keys()
            csv_writer.writerow(header)
            count += 1
        
    csv_writer.writerow(workout.values())
data_file.close()

#converting csv file to panda dataframe
df = pd.read_csv('workout_data.csv')

# converts the timestamp to datetime format
df['timestamp_ms'] = pd.to_datetime(df.timestamp_ms, unit='ms')

# substring operation to pull in the first 8 characters
df['photos'] = df['photos'].str.slice(0,8)

# variable to stored filtered rows with matching substring
pics = df[df['photos'].str.contains("'uri':")]

print(pics)

#print(df[['sender_name','timestamp_ms', 'pics']])


"""
todo
1) Issue w/ column name between 'content' and 'photos' 
"""