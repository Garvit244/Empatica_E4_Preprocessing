import pandas as pd
import os

from main.extra.Interpolate import Interpolate


class Feature_generation():
    def __init__(self, input_dir, gps_dir):
        self.input_dir = input_dir
        self.gps_dir = gps_dir

    def statistical_env_feature(self):
        pd_data = pd.read_csv(self.input_dir + '/Interpolated_Data_w_tags.csv')
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
        pd_data.to_csv(self.input_dir + "/Interpolated_Data_w_tags.csv", index=False)


    def add_walking_features(self):
        gps_file = self.gps_dir + '/GPS.csv'
        columns = ['Epoc_Local', 'Time', 'E4_EDA',  'E4_TEMP', 'E4_HR',
         'Humidity', 'Temperature', 'Pressure', 'Light',
         'IR Temperature', 'Noise', 'Tags', 'SCR', 'SCR_Count',
         'EDA_Peak', 'Rise_Time', 'Max_Deriv', 'Ampl', 'Decay_Time',
         'SCR_width', 'AUC', 'Segment_Mean_Temp', 'Segment_Std_Temp',
         'Segment_Mean_Humi', 'Segment_Std_Humi', 'Segment_Mean_Pressure',
         'Segment_Std_Pressure', 'Segment_Mean_Light', 'Segment_Std_Light',
         'Segment_Mean_Noise', 'Segment_Std_Noise', 'Scr_Per_Segment']

        pd_data = pd.read_csv(self.input_dir + '/Interpolated_Data_w_tags.csv', names=columns)

        if os.path.exists(file_path):
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
            merged_df.to_csv(self.input_dir + "/Interpolated_Data_w_tags.csv")


if __name__ == '__main__':
    dates = ['14_March', '15_March', '16_March', '17_March', '19_March']
    # dates = ['20_March']
    column_names = ['Speed', 'Lng', 'Lat']
    
    for date_val in dates:
        print date_val
        file_path = '/home/striker/Dropbox/NSE_2018_e4/Simei_Morning_Trips/' + date_val + '/Francisco/Results'
        gps_path = '/home/striker/Dropbox/NSE_2018_e4/Simei_Morning_Trips/' + date_val + '/Francisco/GPS'
        f = Feature_generation(file_path, gps_path)
        # f.statistical_env_feature()
        # f.add_walking_features()

        interpolate = Interpolate(file_path + "/Interpolated_Data_w_tags.csv", column_names)
        interpolate.interpolate()

