from main.downsampling.MergerEDAEnivronment import Merger
from main.extra.Feature_generation import Feature_generation
from main.extra.Features import Features
from main.extra.Merger import MergeOtherSensor
from main.extra.TimeConvertor import TimeZoneConvertor
import os
import pandas as pd


class Aggregater:
    def __init__(self, main_dir):
        self.main_dir = main_dir

    def remove_files(self, index):
        os.remove(self.main_dir + '/Results/Merged_EDA.csv')
        os.remove(self.main_dir + '/Results/Combined_Data_' + str(index) + '.csv')

    def aggregate_e4_sensor(self, index, sensor_file):
        output_results = self.main_dir + "/Results"

        if not os.path.exists(output_results):
            os.makedirs(output_results)

        eda_dir_path = self.main_dir + "/EDA"
        merge = Merger(eda_dir_path, output_results)
        merge.create_E4_pd()

        converted_sensor = self.main_dir + "/SENSG/converted-sensor_" + str(index) + ".csv"
        input_sensor = self.main_dir + "/SENSG/"+  str(sensor_file)+ ".csv"
        zone_convertor = TimeZoneConvertor(input_sensor, converted_sensor)
        zone_convertor.convert()

        columns = "Epoc_Local, Readable_Time, E4_EDA, E4_TEMP, E4_HR, Humidity, Temperature, Pressure, Light, IR Temperature, Noise\n"
        input_e4 = output_results + "/Merged_EDA.csv"
        merge_other = MergeOtherSensor(converted_sensor, input_e4, output_results, self.main_dir)

        intermediate_files = "/Combined_Data_" + str(index) + ".csv"
        merge_other.merger_files(columns , intermediate_files)

        output_file = "/Data_w_tags_" + str(index) + ".csv"
        merge_other.add_tags(intermediate_files, output_file)

        merge_other.addscr_tofile(output_file)
        interpolated_file = "/Interpolated_Data_w_tags_" + str(index) + ".csv"
        merge_other.interpolate(interpolated_file=interpolated_file, tag_file=output_file)

        merge_other.add_peaks_tofile(output_file)
        merge_other.add_peaks_tofile(interpolated_file)



if __name__ == '__main__':
    main_dir = "/home/striker/Dropbox/NSE_2018_e4/Tampines/6_April/Francesco/"
    gps_file = main_dir + "/GPS/GPS.csv"

    scr_list = pd.read_excel(io = main_dir + "/Results/SCR.xls", sheetname='CDA')
    scr_list.to_csv(main_dir + "/Results/SCR.csv", index=False, header=False)

    aggregate = Aggregater(main_dir)
    numberOfSensor = 2

    for index in range(1, numberOfSensor+1):
        print index
        sensor_file = 'sensor_data_'
        sensor_file += str(index)
        aggregate.aggregate_e4_sensor(index, sensor_file)
        aggregate.remove_files(index)

        Features().generate_feature(main_dir+ "/Results/Interpolated_Data_w_tags_" + str(index) + ".csv", gps_file)

    users = ['Francisco', 'Garvit', 'Sarah', 'Iman', 'Francesco', 'Darshan']
    for user in users:
        print "Processing User: ", user
        directory = '/home/striker/Dropbox/NSE_2018_e4/Tampines/6_April/' + user + '/Results/'

        file_to_use = 0
        max_rows = float('-inf')

        for file in os.listdir(directory):
            if file.startswith('Data_w_tags_'):
                pd_a = pd.read_csv(os.path.join(directory, file))
                count = pd_a.count().to_dict()[' Noise']
                if count > max_rows:
                    max_rows = count
                    file_to_use = file[-5:][0]
        print 'Using file Number ', file_to_use

        feature_generation = Feature_generation(directory + '/Interpolated_Data_w_tags_' + str(file_to_use) + ".csv",
                                                gps_path=gps_file)

        for windows in range(3,6):
            output_dir = directory + '/Window_Data/'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            feature_generation.add_stastical_features(window=windows, output_path=output_dir+'Data_for_window_' + str(windows) + '.csv')
