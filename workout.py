import json
import csv
import datetime
import pandas as pd

with open(r'C:\Users\chris\OneDrive\Desktop\message_1.json') as json_file:
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
df['content'] = df['content'].str.slice(0,8)

# variable to stored filtered rows with matching substring
pics = df[df['content'].str.contains("'uri':")]

print(pics)

#print(df[['sender_name','timestamp_ms', 'pics']])


"""
todo
1) Use csv or panda dataframe libaries to filter for rows where 'URI' key exists
2) Convert python timestamp to datetime
"""