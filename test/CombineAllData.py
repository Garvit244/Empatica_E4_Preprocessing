from main.downsampling.MergerEDAEnivronment import Merger
from main.extra.Merger import MergeOtherSensor
from main.extra.TimeConvertor import TimeZoneConvertor
import os

if __name__ == '__main__':
    main_dir = "/home/striker/Dropbox/NSE_2018_e4/Simei Morning Trips/15_March/Francisco"
    output_results = main_dir + "/Results"

    if not os.path.exists(output_results):
        os.makedirs(output_results)

    eda_dir_path = main_dir + "/EDA"
    merge = Merger(eda_dir_path, output_results)
    merge.create_E4_pd()

    converted_sensor = main_dir + "/SENSG/converted-sensor.csv"
    input_sensor = main_dir + "/SENSG/environmental-sensor-feed_2018-03-15_09_33_45.csv"
    zone_convertor = TimeZoneConvertor(input_sensor, converted_sensor)
    zone_convertor.convert()

    columns = "Epoc_Local, Readable_Time, E4_EDA, E4_TEMP, E4_HR, Humidity, Temperature, Pressure, Light, IR Temperature, Noise\n"
    input_e4 = output_results + "/Merged_EDA.csv"
    merge_other = MergeOtherSensor(converted_sensor, input_e4, output_results)
    merge_other.merger_files(columns)
