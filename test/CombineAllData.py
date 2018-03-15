from main.downsampling.MergerEDAEnivronment import Merger
from main.extra.Merger import MergeOtherSensor
from main.extra.TimeConvertor import TimeZoneConvertor
import pandas as pd
import os

class Aggregater:
    def __init__(self, main_dir):
        self.main_dir = main_dir

    def aggregate_e4_sensor(self):
        output_results = self.main_dir + "/Results"

        if not os.path.exists(output_results):
            os.makedirs(output_results)

        eda_dir_path = self.main_dir + "/EDA"
        merge = Merger(eda_dir_path, output_results)
        merge.create_E4_pd()

        converted_sensor = self.main_dir + "/SENSG/converted-sensor.csv"
        input_sensor = self.main_dir + "/SENSG/environmental-sensor-feed_2018-03-15_17_28_32.csv"
        zone_convertor = TimeZoneConvertor(input_sensor, converted_sensor)
        zone_convertor.convert()

        columns = "Epoc_Local, Readable_Time, E4_EDA, E4_TEMP, E4_HR, Humidity, Temperature, Pressure, Light, IR Temperature, Noise\n"
        input_e4 = output_results + "/Merged_EDA.csv"
        merge_other = MergeOtherSensor(converted_sensor, input_e4, output_results)
        merge_other.merger_files(columns)

    def add_tags(self):
        tag_file = self.main_dir + "/EDA/tags_labeled.csv"
        pd_tags = pd.read_csv(tag_file, header=None)
        pd_A = pd.read_csv(self.main_dir + "/Results/Combined_Data.csv")

        pd_result = pd.DataFrame()
        tag = "None"
        prev_time = 0

        for index, row in pd_tags.iterrows():
            data = pd_A[(prev_time <= pd_A['Epoc_Local']) &  (pd_A['Epoc_Local'] < row[0])]
            data['Tags']= tag

            if not data.empty:
                pd_result = pd_result.append(data)

            tag = row[1]
            prev_time = row[0]

        data = pd_A[pd_A['Epoc_Local'] >= prev_time]
        data['Tags'] = tag

        if not data.empty:
            pd_result = pd_result.append(data)

        pd_result.to_csv(self.main_dir + "/Results/Data_w_tags.csv")
        print len(pd_result), len(pd_A)

if __name__ == '__main__':
    main_dir = "/home/striker/Dropbox/NSE_2018_e4/NoSpecificLocation/15_march/Darshan"
    aggregate = Aggregater(main_dir)
    aggregate.aggregate_e4_sensor()
    aggregate.add_tags()