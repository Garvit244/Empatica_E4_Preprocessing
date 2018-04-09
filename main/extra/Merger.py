import pandas as pd
from datetime import datetime, timedelta

class MergeOtherSensor:
    def __init__(self, input_sensor_file, input_e4_file, output_dir, main_dir):
        self.input_sensor_file = input_sensor_file
        self.input_e4_file = input_e4_file
        self.output_dir = output_dir
        self.main_dir = main_dir

    def string_to_datetime(self, datetime_obj):
        return datetime.strptime(datetime_obj, '%H:%M:%S')

    def merger_files(self, columns, file_name):
        output_file = open(self.output_dir + file_name, 'w')
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


    def add_tags(self, file_name, output_file):
        tag_file = self.main_dir + "/EDA/tags_labeled.csv"
        pd_tags = pd.read_csv(tag_file, header=None)
        pd_A = pd.read_csv(self.main_dir + "/Results"+ file_name)

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

        pd_result.to_csv(self.main_dir + "/Results" + output_file)

    def addscr_tofile(self, tag_file):
        data_file = pd.read_csv(self.main_dir + "/Results" + tag_file)
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

                count += 1
                if cur_index < len(scr_list) -1:
                    scr_time = int(scr_list[cur_index][0] + time_start)

            scr_count = scr_count.append(pd.DataFrame([count]))
            scr_dataframe = scr_dataframe.append(pd.DataFrame([scr_value]))

        data_file['SCR'] = scr_dataframe.values
        data_file['SCR_Count'] = scr_count.values
        data_file = data_file.drop([u'Unnamed: 0'], axis=1)
        data_file.to_csv(self.main_dir + "/Results" + tag_file, index= False)

    def interpolate(self, tag_file, interpolated_file):
        pd_output = pd.read_csv(self.main_dir + '/Results' + tag_file)

        pd_output = pd_output.fillna(method='ffill')
        pd_output.to_csv(self.main_dir + '/Results' + interpolated_file, index= False)


    def add_peaks_tofile(self, file_name):
        peak_file = pd.read_csv(self.main_dir + "/Results/Peak.csv")
        peak_file.columns = ['EDA_Time', 'EDA_PEAK', 'Rise_Time', 'Max_Deriv', 'Ampl', 'Decay_Time', 'SCR_width', 'AUC']
        peak_file['EDA_Time'] = peak_file['EDA_Time'].astype(datetime)

        mapped_time = pd.DataFrame()
        for index, row in peak_file.iterrows():
            row_split = row[0].split(".")
            new_time = (datetime.strptime(row_split[0], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)).strftime("%H:%M:%S")
            mapped_time = mapped_time.append(pd.DataFrame([new_time]))

        peak_file = peak_file.drop(['EDA_Time'], axis=1)
        peak_file['Peak_Time'] = mapped_time.values

        data_file = pd.read_csv(self.main_dir + "/Results" + file_name)

        EDA_PEAK_df = pd.DataFrame()
        Rise_Time_df = pd.DataFrame()
        Max_Deriv_df = pd.DataFrame()
        Ampl_df = pd.DataFrame()
        Decay_Time_df = pd.DataFrame()
        SCR_width_df = pd.DataFrame()
        AUC_df = pd.DataFrame()

        for index, row in data_file.iterrows():
            peak_data = peak_file[peak_file['Peak_Time'] == row[1]]

            EDA_PEAK = -1
            Rise_Time = -1
            Max_Deriv = -1
            Ampl = -1
            Decay_Time = -1
            SCR_width = -1
            AUC = -1

            if not peak_data.empty:
                EDA_PEAK = peak_data['EDA_PEAK'].values[0]
                Rise_Time = peak_data['Rise_Time'].values[0]
                Max_Deriv = peak_data['Max_Deriv'].values[0]
                Ampl = peak_data['Ampl'].values[0]
                Decay_Time = peak_data['Decay_Time'].values[0]
                SCR_width = peak_data['SCR_width'].values[0]
                AUC = peak_data['AUC'].values[0]

            EDA_PEAK_df = EDA_PEAK_df.append(pd.DataFrame([EDA_PEAK]))
            Rise_Time_df = Rise_Time_df.append(pd.DataFrame([Rise_Time]))
            Max_Deriv_df = Max_Deriv_df.append(pd.DataFrame([Max_Deriv]))
            Ampl_df = Ampl_df.append(pd.DataFrame([Ampl]))
            Decay_Time_df = Decay_Time_df.append(pd.DataFrame([Decay_Time]))
            SCR_width_df = SCR_width_df.append(pd.DataFrame([SCR_width]))
            AUC_df = AUC_df.append(pd.DataFrame([AUC]))

        data_file['EDA_Peak'] = EDA_PEAK_df.values
        data_file['Rise_Time'] = Rise_Time_df.values
        data_file['Max_Deriv'] = Max_Deriv_df.values
        data_file['Ampl'] = Ampl_df.values
        data_file['Decay_Time'] = Decay_Time_df.values
        data_file['SCR_width'] = SCR_width_df.values
        data_file['AUC'] = AUC_df.values

        data_file.to_csv(self.main_dir + "/Results" + file_name, index=False)
