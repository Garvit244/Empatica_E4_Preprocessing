import pandas as pd
from datetime import datetime, timedelta
import re
import numpy as np

class SensorE4Merger:
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

    def clean(self, columns_filter, date_col, pressure_col):
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
        cleaned_df[pressure_col] = cleaned_df[pressure_col].str.replace(',','').astype('float')

        return cleaned_df[columns_filter]

    def mergeSensorFile(self, columns_filter, date_col, pressure_col):
        pd_empatica = pd.read_csv(self.input_e4_file)
        pd_sensor = self.clean(columns_filter, date_col, pressure_col)
        pd_result = pd_empatica.merge(pd_sensor.rename(columns={date_col: 'Epoc_Time'}), how='left')
        pd_result = pd_result.fillna(method='ffill')
        pd_result.to_csv(self.input_e4_file, index=False)


    def add_tags(self, tags_file):
        pd_tags = pd.read_csv(tags_file, header=None)
        pd_merged = pd.read_csv(self.input_e4_file)

        pd_result = pd.DataFrame()
        tag = "0"
        lap = "Lap 1"
        prev_time = 0

        for index, row in pd_tags.iterrows():
            data = pd_merged[(prev_time <= pd_merged['Epoc_Time']) & (pd_merged['Epoc_Time'] < (row[0] + 8*60*60))]
            data['Tags'] = tag
            data['Lap'] = lap

            if not data.empty:
                pd_result = pd_result.append(data)

            tag, lap = row[1], row[2]
            prev_time = (row[0] + 8*60*60)

        data = pd_merged[pd_merged['Epoc_Time'] >= prev_time]
        data['Tags'] = tag
        data['Lap'] = lap

        if not data.empty:
            pd_result = pd_result.append(data)

        pd_result.to_csv(self.input_e4_file, index=False)

    def getStartingTime(self):
        pd_a = pd.read_csv(self.input_e4_file)
        return pd_a['Epoc_Time'][0]

    def addscr_tofile(self, scr_file):
        pd_a = pd.read_csv(self.input_e4_file)
        start_time = pd_a['Epoc_Time'][0]
        scr_list = pd.read_excel(scr_file, sheet_name='CDA')

        scr_list["CDA.SCR-Onset"]  = (scr_list["CDA.SCR-Onset"] + start_time).astype('int')
        scr_mean = scr_list.groupby(['CDA.SCR-Onset'], as_index=False).mean()
        scr_mean['Count'] = pd.DataFrame(scr_list.groupby(['CDA.SCR-Onset'], as_index=False).size().values)

        pd_result = pd_a.merge(scr_mean.rename(columns={"CDA.SCR-Onset":"Epoc_Time"}), how='left')
        pd_result = pd_result.fillna(0)
        pd_result.to_csv(self.input_e4_file, index=False)

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
