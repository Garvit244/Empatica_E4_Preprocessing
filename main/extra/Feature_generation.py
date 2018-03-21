import pandas as pd

class Feature_generation():
    def __init__(self, input_dir):
        self.input_dir = input_dir

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

            count_scr = len(tag_dataframe.iloc[:,12].nonzero()[0])

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


if __name__ == '__main__':
    f = Feature_generation('/home/striker/Dropbox/NSE_2018_e4/Simei_Morning_Trips/20_March/Francisco/Results')
    f.statistical_env_feature()