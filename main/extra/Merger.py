import pandas as pd
from datetime import datetime, timedelta
import re
import numpy as np

class MergeOtherSensor:
    def __init__(self, input_sensor_file, input_e4_file, output_dir, main_dir):
        self.input_e4_file = input_e4_file
        self.pd = pd.read_csv(input_sensor_file, header=None)
        self.output_dir = output_dir
        self.main_dir = main_dir

    def string_to_datetime(self, datetime_obj):
        return datetime.strptime(datetime_obj, '%H:%M:%S')

    def checkValidity(self ,row):
        count = 0
        for index, value in row.iterrows():
            value = str(value)
            if re.search('[a-zA-Z]+', value).group() != 'Name':
                count += 1

        if count == len(row)-1:
            return False
        return True

    def clean(self, columns_filter, date_col):
        columns, cleaned_df = pd.DataFrame(), pd.DataFrame()
        column_find  = False

        for index, row in self.pd.iterrows():
            row = pd.DataFrame(row)
            if columns.empty:
                columns = row
            else:
                if columns.isnull().values.any():
                    columns = row
                else:
                    if not column_find:
                        cleaned_df = cleaned_df.append(columns.T)
                        cleaned_df = cleaned_df.drop(cleaned_df.index[0])
                        column_find = True
                    else:
                        if self.checkValidity(row):
                            cleaned_df = cleaned_df.append(row.T)

        cleaned_df.columns = np.array(columns.values).flatten().tolist()
        cleaned_df[date_col] = pd.DataFrame(pd.to_datetime(cleaned_df[date_col]).view('int64')/pow(10,9)).astype('int')

        return cleaned_df[columns_filter]

    def mergeSensorFile(self, columns_filter, date_col):
        pd_empatica = pd.read_csv(self.input_e4_file)
        pd_sensor = self.clean(columns_filter, date_col)
        pd_result = pd_empatica.merge(pd_sensor.rename(columns={date_col: 'Epoc_Time'}), how='left')
        pd_result.to_csv(self.input_e4_file, index=False)


    # def add_tags(self, file_name, output_file):
    #     tag_file = self.main_dir + "/EDA/tags_labeled.csv"
    #     pd_tags = pd.read_csv(tag_file, header=None)
    #     pd_A = pd.read_csv(self.main_dir + "/Results"+ file_name)
    #
    #     pd_result = pd.DataFrame()
    #     tag = "None"
    #     prev_time = 0
    #
    #     for index, row in pd_tags.iterrows():
    #         data = pd_A[(prev_time <= pd_A['Epoc_Local']) & (pd_A['Epoc_Local'] < (row[0]))]
    #         data['Tags'] = tag
    #
    #         if not data.empty:
    #             pd_result = pd_result.append(data)
    #
    #         tag = row[1]
    #         prev_time = (row[0])
    #
    #     data = pd_A[pd_A['Epoc_Local'] >= prev_time]
    #     data['Tags'] = tag
    #
    #     if not data.empty:
    #         pd_result = pd_result.append(data)
    #
    #     pd_result.to_csv(self.main_dir + "/Results" + output_file)
    #
    # def addscr_tofile(self, tag_file):
    #     data_file = pd.read_csv(self.main_dir + "/Results" + tag_file)
    #     scr_list = pd.read_csv(self.main_dir + "/Results/SCR.csv", header=None)
    #     scr_list[0] = scr_list[0].astype(int)
    #     scr_list = scr_list.values.tolist()
    #     cur_index = 0
    #     time_start = data_file.iloc[0][1]
    #     scr_time = int(scr_list[cur_index][0] + time_start)
    #
    #     scr_dataframe = pd.DataFrame()
    #     scr_count = pd.DataFrame()
    #
    #     for index, row in data_file.iterrows():
    #         epoc_time = row[1]
    #         scr_value = 0
    #         count = 0
    #
    #         if epoc_time == scr_time:
    #             scr_value = scr_list[cur_index][1]
    #             cur_index += 1
    #
    #             while cur_index < len(scr_list)-1:
    #                 if scr_list[cur_index][0] != scr_list[cur_index+1][0]:
    #                     break
    #                 cur_index += 1
    #                 count += 1
    #
    #             count += 1
    #             if cur_index < len(scr_list) -1:
    #                 scr_time = int(scr_list[cur_index][0] + time_start)
    #
    #         scr_count = scr_count.append(pd.DataFrame([count]))
    #         scr_dataframe = scr_dataframe.append(pd.DataFrame([scr_value]))
    #
    #     data_file['SCR'] = scr_dataframe.values
    #     data_file['SCR_Count'] = scr_count.values
    #     data_file = data_file.drop([u'Unnamed: 0'], axis=1)
    #     data_file.to_csv(self.main_dir + "/Results" + tag_file, index= False)
    #
    # def interpolate(self, tag_file, interpolated_file):
    #     pd_output = pd.read_csv(self.main_dir + '/Results' + tag_file)
    #
    #     pd_output = pd_output.fillna(method='ffill')
    #     pd_output.to_csv(self.main_dir + '/Results' + interpolated_file, index= False)
    #
    #
    # def add_peaks_tofile(self, file_name):
    #     peak_file = pd.read_csv(self.main_dir + "/Results/Peak.csv")
    #     peak_file.columns = ['EDA_Time', 'EDA_PEAK', 'Rise_Time', 'Max_Deriv', 'Ampl', 'Decay_Time', 'SCR_width', 'AUC']
    #     peak_file['EDA_Time'] = peak_file['EDA_Time'].astype(datetime)
    #
    #     mapped_time = pd.DataFrame()
    #     for index, row in peak_file.iterrows():
    #         row_split = row[0].split(".")
    #         new_time = (datetime.strptime(row_split[0], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)).strftime("%H:%M:%S")
    #         mapped_time = mapped_time.append(pd.DataFrame([new_time]))
    #
    #     peak_file = peak_file.drop(['EDA_Time'], axis=1)
    #     peak_file['Peak_Time'] = mapped_time.values
    #
    #     data_file = pd.read_csv(self.main_dir + "/Results" + file_name)
    #
    #     EDA_PEAK_df = pd.DataFrame()
    #     Rise_Time_df = pd.DataFrame()
    #     Max_Deriv_df = pd.DataFrame()
    #     Ampl_df = pd.DataFrame()
    #     Decay_Time_df = pd.DataFrame()
    #     SCR_width_df = pd.DataFrame()
    #     AUC_df = pd.DataFrame()
    #
    #     for index, row in data_file.iterrows():
    #         peak_data = peak_file[peak_file['Peak_Time'] == row[1]]
    #
    #         EDA_PEAK = -1
    #         Rise_Time = -1
    #         Max_Deriv = -1
    #         Ampl = -1
    #         Decay_Time = -1
    #         SCR_width = -1
    #         AUC = -1
    #
    #         if not peak_data.empty:
    #             EDA_PEAK = peak_data['EDA_PEAK'].values[0]
    #             Rise_Time = peak_data['Rise_Time'].values[0]
    #             Max_Deriv = peak_data['Max_Deriv'].values[0]
    #             Ampl = peak_data['Ampl'].values[0]
    #             Decay_Time = peak_data['Decay_Time'].values[0]
    #             SCR_width = peak_data['SCR_width'].values[0]
    #             AUC = peak_data['AUC'].values[0]
    #
    #         EDA_PEAK_df = EDA_PEAK_df.append(pd.DataFrame([EDA_PEAK]))
    #         Rise_Time_df = Rise_Time_df.append(pd.DataFrame([Rise_Time]))
    #         Max_Deriv_df = Max_Deriv_df.append(pd.DataFrame([Max_Deriv]))
    #         Ampl_df = Ampl_df.append(pd.DataFrame([Ampl]))
    #         Decay_Time_df = Decay_Time_df.append(pd.DataFrame([Decay_Time]))
    #         SCR_width_df = SCR_width_df.append(pd.DataFrame([SCR_width]))
    #         AUC_df = AUC_df.append(pd.DataFrame([AUC]))
    #
    #     data_file['EDA_Peak'] = EDA_PEAK_df.values
    #     data_file['Rise_Time'] = Rise_Time_df.values
    #     data_file['Max_Deriv'] = Max_Deriv_df.values
    #     data_file['Ampl'] = Ampl_df.values
    #     data_file['Decay_Time'] = Decay_Time_df.values
    #     data_file['SCR_width'] = SCR_width_df.values
    #     data_file['AUC'] = AUC_df.values
    #
    #     data_file.to_csv(self.main_dir + "/Results" + file_name, index=False)
