import pandas as pd
import numpy as np
import os

from main.extra.Interpolate import Interpolate


class Feature_generation():
    def __init__(self, input_path, gps_path):
        self.input_path = input_path
        self.gps_path = gps_path

    def statistical_env_feature(self):
        pd_data = pd.read_csv(self.input_path)
        tags = pd_data.iloc[:, 11].unique()

        mean_humidity_df = pd.DataFrame()
        mean_temperature_df = pd.DataFrame()
        mean_pressure_df = pd.DataFrame()
        mean_light_df = pd.DataFrame()
        mean_noise_df = pd.DataFrame()

        std_humidity_df = pd.DataFrame()
        std_temperature_df = pd.DataFrame()
        std_pressure_df = pd.DataFrame()
        std_light_df = pd.DataFrame()
        std_noise_df = pd.DataFrame()

        count_scr_segment_df = pd.DataFrame()

        for tag in tags:
            tag_dataframe = pd_data[pd_data.iloc[:, 11] == tag]
            mean_humidity = tag_dataframe.iloc[:,5].mean()
            mean_temp = tag_dataframe.iloc[:,6].mean()
            mean_pressure = tag_dataframe.iloc[:,7].mean()
            mean_light = tag_dataframe.iloc[:,8].mean()
            mean_noise = tag_dataframe.iloc[:,10].mean()


            std_humidity = tag_dataframe.iloc[:, 5].std()
            std_temp = tag_dataframe.iloc[:, 6].std()
            std_pressure = tag_dataframe.iloc[:, 7].std()
            std_light = tag_dataframe.iloc[:, 8].std()
            std_noise = tag_dataframe.iloc[:, 10].std()

            count_scr = len(tag_dataframe.iloc[:,13].nonzero()[0])

            for index in range(len(tag_dataframe)):
                mean_humidity_df = mean_humidity_df.append(pd.DataFrame([mean_humidity]))
                std_humidity_df = std_humidity_df.append(pd.DataFrame([std_humidity]))

                mean_temperature_df = mean_temperature_df.append(pd.DataFrame([mean_temp]))
                std_temperature_df = std_temperature_df.append(pd.DataFrame([std_temp]))

                mean_pressure_df = mean_pressure_df.append(pd.DataFrame([mean_pressure]))
                std_pressure_df = std_pressure_df.append(pd.DataFrame([std_pressure]))

                mean_light_df = mean_light_df.append(pd.DataFrame([mean_light]))
                std_light_df = std_light_df.append(pd.DataFrame([std_light]))

                mean_noise_df = mean_noise_df.append(pd.DataFrame([mean_noise]))
                std_noise_df = std_noise_df.append(pd.DataFrame([std_noise]))

                count_scr_segment_df = count_scr_segment_df.append(pd.DataFrame([count_scr]))


        pd_data['Segment_Mean_Temp'] = mean_temperature_df.values
        pd_data['Segment_Std_Temp'] = std_temperature_df.values

        pd_data['Segment_Mean_Humi'] = mean_humidity_df.values
        pd_data['Segment_Std_Humi'] = std_humidity_df.values

        pd_data['Segment_Mean_Pressure'] = mean_pressure_df.values
        pd_data['Segment_Std_Pressure'] = std_pressure_df.values

        pd_data['Segment_Mean_Light'] = mean_light_df.values
        pd_data['Segment_Std_Light'] = std_light_df.values

        pd_data['Segment_Mean_Noise'] = mean_noise_df.values
        pd_data['Segment_Std_Noise'] = std_noise_df.values

        pd_data['Scr_Per_Segment'] = count_scr_segment_df.values
        pd_data.to_csv(self.input_path, index=False)


    def add_walking_features(self, columns):
        gps_file = self.gps_path
        pd_data = pd.read_csv(self.input_path, names=columns)

        if os.path.exists(self.gps_path):
            pd_gps = pd.read_csv(gps_file)
            new_pd = pd_gps[['Time', 'Speed', 'Lat', 'Lng']]
            time_df = new_pd['Time'].values
            time_series = pd.DataFrame()

            for time in time_df:
                new_time = time.split('T')[1].split('.')[0]
                time_series = time_series.append(pd.DataFrame([new_time]))

            new_pd = new_pd.drop(['Time'], axis=1)
            new_pd['Time'] = time_series.values

            merged_df = pd_data.set_index('Time').join(new_pd.set_index('Time'))
            merged_df = merged_df[1:]
            print len(merged_df), len(pd_data)
            merged_df.to_csv(self.input_path)

    def generate_stats(self, data):
        avg = data.mean()
        std = data.std()
        minimum = data.min()
        maximum = data.max()

        return avg, std, minimum, maximum

    def add_stastical_features(self, window, output_path):
        pd_data = pd.read_csv(self.input_path)

        pd_output = pd.DataFrame()
        for index, row in pd_data.iterrows():
            scr_value = row['SCR']
            tag = row['Tags']
            if float(scr_value) != 0.0:
                print scr_value
                if index < (window/2):
                    data = pd_data.iloc[index:index + (window / 2) + 1, :21]
                else:
                    data = pd_data.iloc[index-(window/2):index + (window / 2) + 1, :21]


                corresponding_reading = pd_data.iloc[index, :5]
                avg, std, minimum, maximum = self.generate_stats(data[['Humidity', 'Temperature', 'Pressure',
                                                                       'Noise', 'Light', 'IR Temperature',
                                                                       'Rise_Time', 'Max_Deriv', 'Ampl',
                                                                       'Decay_Time', 'SCR_width', 'AUC']])
                number_scr = data['SCR_Count'].sum()
                number_of_peak = data[data['EDA_Peak'] != -1].sum()['EDA_Peak']
                final_series = pd.concat([corresponding_reading, avg, std, minimum, maximum])
                final_series = final_series.append(pd.Series([scr_value, number_scr, number_of_peak, tag]))
                calc_data = final_series.to_frame().reset_index().T.iloc[1:, :]

                pd_output = pd_output.append(calc_data)

        pd_output.columns = ['Epoc_Local', 'Readable_Time', 'E4_EDA', 'E4_TEMP', 'E4_HR', 'Avg_Humi', 'Avg_Tem',
                             'Avg_Pre', 'Avg_Noise', 'Avg_Light', 'Avg_IR', 'Avg_Rise_time', 'Avg_Max_Deriv',
                             'Avg_Ampl', 'Avg_Decay', 'Avg_SCR_width', 'Avg_AUC', 'STD_Humi', 'STD_Tem','STD_Pre',
                             'STD_Noise', 'STD_Light', 'STD_IR', 'STD_Rise_time', 'STD_Max_Deriv','STD_Ampl',
                             'STD_Decay', 'STD_SCR_width', 'STD_AUC', 'MIN_Humi', 'MIN_Tem','MIN_Pre', 'MIN_Noise',
                             'MIN_Light', 'MIN_IR', 'MIN_Rise_time', 'MIN_Max_Deriv','MIN_Ampl', 'MIN_Decay',
                             'MIN_SCR_width', 'MIN_AUC','MAX_Humi', 'MAX_Tem','MAX_Pre', 'MAX_Noise', 'MAX_Light',
                             'MAX_IR', 'MAX_Rise_time', 'MAX_Max_Deriv','MAX_Ampl', 'MAX_Decay', 'MAX_SCR_width',
                             'MAX_AUC', 'SCR_Value', 'SCR_Count', 'Peak_Count', 'Tag']

        pd_output.to_csv(output_path, index=False)

