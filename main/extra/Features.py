from main.extra.Feature_generation import Feature_generation
from main.extra.Interpolate import Interpolate


class Features:
    def generate_feature(self, file_path, gps_path):
        column_names = ['Speed', 'Lng', 'Lat']
        columns = ['Epoc_Local', 'Time', 'E4_EDA', 'E4_TEMP', 'E4_HR',
                   'Humidity', 'Temperature', 'Pressure', 'Light',
                   'IR Temperature', 'Noise', 'Tags', 'SCR', 'SCR_Count',
                   'EDA_Peak', 'Rise_Time', 'Max_Deriv', 'Ampl', 'Decay_Time',
                   'SCR_width', 'AUC', 'Segment_Mean_Temp', 'Segment_Std_Temp',
                   'Segment_Mean_Humi', 'Segment_Std_Humi', 'Segment_Mean_Pressure',
                   'Segment_Std_Pressure', 'Segment_Mean_Light', 'Segment_Std_Light',
                   'Segment_Mean_Noise', 'Segment_Std_Noise', 'Scr_Per_Segment']



        f = Feature_generation(file_path, gps_path)
        f.statistical_env_feature()
        f.add_walking_features(columns)

        interpolate = Interpolate(file_path, column_names)
        interpolate.interpolate()
