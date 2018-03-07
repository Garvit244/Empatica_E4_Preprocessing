import pandas as pd
from datetime import datetime

class MergeOtherSensor:
    def __init__(self, input_sensor_file, input_e4_file, output_dir):
        self.input_sensor_file = input_sensor_file
        self.input_e4_file = input_e4_file
        self.output_dir = output_dir

    def string_to_datetime(self, datetime_obj):
        return datetime.strptime(datetime_obj, '%H:%M:%S')

    def merger_files(self, columns):
        output_file = open(self.output_dir + '/Combined_Data.csv', 'w')
        output_file.write(columns)

        pd_empatica = pd.read_csv(self.input_e4_file)
        pd_sensor = pd.read_csv(self.input_sensor_file)

        print 'Number of reading before removing redundant reading ', len(pd_sensor)
        pd_sensor = pd_sensor.groupby(pd_sensor.iloc[:, 0]).mean().reset_index()
        print 'Number of reading after removing redundant reading ', len(pd_sensor)

        for index, row in pd_empatica.iterrows():
            sensor_data = pd_sensor[pd_sensor['Time'] == row[1]]
            temp = -1
            pressure = -1
            light = -1
            ir_temp = -1
            noise = -1
            humidity = -1

            if not sensor_data.empty:
                sensor_data = sensor_data.values[0]
                temp = sensor_data[2]
                humidity = sensor_data[1]
                pressure = sensor_data[3]
                light = sensor_data[4]
                ir_temp = sensor_data[5]
                noise = sensor_data[6]

            output_file.write(str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4]) + ',' + str(humidity) +
                              ',' + str(temp) + ',' + str(pressure) + ',' + str(light) + ',' + str(ir_temp) + ',' +
                              str(noise) + '\n')
