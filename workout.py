import json
import csv
#import pandas

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