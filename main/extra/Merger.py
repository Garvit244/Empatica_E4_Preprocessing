import pandas as pd
from datetime import datetime
import  time
class MergeOtherSensor:
    def __init__(self, input_sensor_file, input_e4_file, output_dir, main_dir):
        self.input_sensor_file = input_sensor_file
        self.input_e4_file = input_e4_file
        self.output_dir = output_dir
        self.main_dir = main_dir

    def string_to_datetime(self, datetime_obj):
        return datetime.strptime(datetime_obj, '%H:%M:%S')

    def merger_files(self, columns):
        output_file = open(self.output_dir + '/Combined_Data.csv', 'w')
        output_file.write(columns)

        pd_empatica = pd.read_csv(self.input_e4_file)
        pd_sensor = pd.read_csv(self.input_sensor_file)

        print 'Number of reading before removing redundant reading ', len(pd_sensor)
        pd_sensor = pd_sensor.groupby(pd_sensor.iloc[:, 0]).mean()
        pd_sensor['Time'] = pd_sensor.index
        print 'Number of reading after removing redundant reading ', len(pd_sensor)

        for index, row in pd_empatica.iterrows():
            sensor_data = pd_sensor[pd_sensor['Time'] == row[1]]
            temp = float('nan')
            pressure = float('nan')
            light = float('nan')
            ir_temp = float('nan')
            noise = float('nan')
            humidity = float('nan')

            if not sensor_data.empty:
                sensor_data = sensor_data.values[0]
                temp = sensor_data[1]
                humidity = sensor_data[0]
                pressure = sensor_data[2]
                light = sensor_data[3]
                ir_temp = sensor_data[4]
                noise = sensor_data[5]

            output_file.write(str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4]) + ',' + str(humidity) +
                              ',' + str(temp) + ',' + str(pressure) + ',' + str(light) + ',' + str(ir_temp) + ',' +
                              str(noise) + '\n')


    def add_tags(self):
        tag_file = self.main_dir + "/EDA/tags_labeled.csv"
        pd_tags = pd.read_csv(tag_file, header=None)
        pd_A = pd.read_csv(self.main_dir + "/Results/Combined_Data.csv")

        pd_result = pd.DataFrame()
        tag = "None"
        prev_time = 0

        for index, row in pd_tags.iterrows():
            data = pd_A[(prev_time <= pd_A['Epoc_Local']) & (pd_A['Epoc_Local'] < (row[0]))]
            data['Tags'] = tag

            if not data.empty:
                pd_result = pd_result.append(data)

            tag = row[1]
            prev_time = (row[0])

        data = pd_A[pd_A['Epoc_Local'] >= prev_time]
        data['Tags'] = tag

        if not data.empty:
            pd_result = pd_result.append(data)

        pd_result.to_csv(self.main_dir + "/Results/Data_w_tags.csv")

    def addscr_tofile(self):
        data_file = pd.read_csv(self.main_dir + "/Results/Data_w_tags.csv")
        scr_list = pd.read_csv(self.main_dir + "/Results/SCR.csv", header=None)
        scr_list[0] = scr_list[0].astype(int)
        scr_list = scr_list.values.tolist()
        cur_index = 0
        time_start = data_file.iloc[0][1]
        scr_time = int(scr_list[cur_index][0] + time_start)

        scr_dataframe = pd.DataFrame()
        scr_count = pd.DataFrame()

        for index, row in data_file.iterrows():
            epoc_time = row[1]
            scr_value = 0
            count = 0

            if epoc_time == scr_time:
                scr_value = scr_list[cur_index][1]
                cur_index += 1

                while cur_index < len(scr_list)-1:
                    if scr_list[cur_index][0] != scr_list[cur_index+1][0]:
                        break
                    cur_index += 1
                    count += 1

                scr_time = int(scr_list[cur_index][0] + time_start)

            scr_count = scr_count.append(pd.DataFrame([count]))
            scr_dataframe = scr_dataframe.append(pd.DataFrame([scr_value]))

        data_file['SCR'] = scr_dataframe.values
        data_file['SCR_Count'] = scr_count.values
        data_file = data_file.drop([u'Unnamed: 0'], axis=1)
        data_file.to_csv(self.main_dir + "/Results/Data_w_tags.csv", index= False)

    def interpolate(self):
        pd_output = pd.read_csv(self.main_dir + '/Results/Data_w_tags.csv')

        pd_output = pd_output.fillna(method='ffill')
        pd_output.to_csv(self.main_dir + '/Results/Interpolated_Data_w_tags.csv')


    def add_peaks_tofile(self):
        peak_file = pd.read_csv(self.main_dir + "/Results/Peaks_0.01.csv")
        peak_file.columns = ['EDA_Time', 'EDA_PEAK', 'Rise_Time', 'Max_Deriv', 'Ampl', 'Decay_Time', 'SCR_width', 'AUC']
        peak_file['EDA_Time'] = peak_file['EDA_Time'].astype(datetime)
        datetime.strptime(peak_file['EDA_Time'][0], '%Y-%m-%d %H:%M:%S')
        print peak_file
