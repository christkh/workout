from datetime import datetime
import arrow

ts = 1642400551271

dt = arrow.Arrow.fromtimestamp(ts)

print(dt.to('US/Pacific').format('MM-DD-YYYY HH:mm:ss'))

#print (dt)

"""
1) specify start of date for range
2) Create weeks with dates as list elements
    ex: W1 [11/08/2021, 11/09/2021],
        W2 [11/15/2021, ...]

3) look up w_date value and assign week value where matching

"""