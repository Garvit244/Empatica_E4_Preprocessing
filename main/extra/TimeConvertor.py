import pandas as pd
from datetime import datetime, timedelta


class TimeZoneConvertor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def convert(self):
        pd_A = pd.read_csv(self.input_file,delimiter=',')

        output = open(self.output_file, 'w')
        output.write("Time, Humidity, Temperature, Pressure, Light, IR Temperature, Noise\n")

        for index, row in pd_A.iterrows():
            value = datetime.fromtimestamp(row[0]/1000)
            value = value - timedelta(hours=8)
            time_s =  value.strftime('%H:%M:%S')
            output.write(str(time_s) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]) + '\n')
