import pandas as pd
from datetime import datetime, timedelta

def convert(pd_A):
    output = open("/home/striker/Downloads/March_6_945.csv", 'w')
    output.write("Time, Humidity, Temperature, Pressure, Light, IR Temperature, Noise\n")

    for index, row in pd_A.iterrows():
        value = datetime.fromtimestamp(row[0]/1000)
        value = value - timedelta(hours=8)
        time_s =  value.strftime('%H:%M:%S')
        output.write(str(time_s) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]) + '\n')


if __name__ == '__main__':
    pd_A = pd.read_csv("/home/striker/Downloads/environmental-sensor-feed_2018-03-06_09_44_17.csv", delimiter=',')
    convert(pd_A)