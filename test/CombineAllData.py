from main.downsampling.MergerEDAEnivronment import Merger
from main.extra.Merger import MergeOtherSensor
from main.extra.TimeConvertor import TimeZoneConvertor
import os
import pandas as pd

class Aggregater:
    def __init__(self, main_dir):
        self.main_dir = main_dir

    def remove_files(self):
        os.remove(self.main_dir + '/Results/Merged_EDA.csv')
        os.remove(self.main_dir + '/Results/Combined_Data.csv')

    def aggregate_e4_sensor(self):
        output_results = self.main_dir + "/Results"

        if not os.path.exists(output_results):
            os.makedirs(output_results)

        eda_dir_path = self.main_dir + "/EDA"
        merge = Merger(eda_dir_path, output_results)
        merge.create_E4_pd()

        converted_sensor = self.main_dir + "/SENSG/converted-sensor.csv"
        input_sensor = self.main_dir + "/SENSG/sensor_data.csv"
        zone_convertor = TimeZoneConvertor(input_sensor, converted_sensor)
        zone_convertor.convert()

        columns = "Epoc_Local, Readable_Time, E4_EDA, E4_TEMP, E4_HR, Humidity, Temperature, Pressure, Light, IR Temperature, Noise\n"
        input_e4 = output_results + "/Merged_EDA.csv"
        merge_other = MergeOtherSensor(converted_sensor, input_e4, output_results, self.main_dir)
        merge_other.merger_files(columns)

        merge_other.add_tags()
        merge_other.addscr_tofile()
        merge_other.interpolate()
        merge_other.add_peaks_tofile("Data_w_tags.csv")
        merge_other.add_peaks_tofile("Interpolated_Data_w_tags.csv")



if __name__ == '__main__':
    main_dir = "/home/striker/Dropbox/NSE_2018_e4/Simei_Morning_Trips/14_March/Francisco"
    # scr_list = pd.read_excel(io = main_dir + "/Results/SCR.xls", sheetname='CDA')
    # scr_list.to_csv(main_dir + "/Results/SCR.csv", index=False, header=False)

    aggregate = Aggregater(main_dir)
    aggregate.aggregate_e4_sensor()
    aggregate.remove_files()

