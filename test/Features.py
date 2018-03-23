from main.extra.Feature_generation import Feature_generation
from main.extra.Interpolate import Interpolate


class Features:
    def generate_feature(self):
        dates = ['14_March', '15_March', '16_March', '17_March', '19_March']
        # dates = ['20_March']
        column_names = ['Speed', 'Lng', 'Lat']
        columns = ['Epoc_Local', 'Time', 'E4_EDA', 'E4_TEMP', 'E4_HR',
                   'Humidity', 'Temperature', 'Pressure', 'Light',
                   'IR Temperature', 'Noise', 'Tags', 'SCR', 'SCR_Count',
                   'EDA_Peak', 'Rise_Time', 'Max_Deriv', 'Ampl', 'Decay_Time',
                   'SCR_width', 'AUC', 'Segment_Mean_Temp', 'Segment_Std_Temp',
                   'Segment_Mean_Humi', 'Segment_Std_Humi', 'Segment_Mean_Pressure',
                   'Segment_Std_Pressure', 'Segment_Mean_Light', 'Segment_Std_Light',
                   'Segment_Mean_Noise', 'Segment_Std_Noise', 'Scr_Per_Segment']

        for date_val in dates:
            print date_val
            file_path = '/home/striker/Dropbox/NSE_2018_e4/Simei_Morning_Trips/' + date_val + '/Francisco/Results/Interpolated_Data_w_tags.csv'
            gps_path = '/home/striker/Dropbox/NSE_2018_e4/Simei_Morning_Trips/' + date_val + '/Francisco/GPS/GPS.cs'

            f = Feature_generation(file_path, gps_path)
            f.statistical_env_feature()
            f.add_walking_features(columns)

            interpolate = Interpolate(file_path, column_names)
            interpolate.interpolate()


if __name__ == '__main__':
    Features().generate_feature()
