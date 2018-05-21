from processing.python.analysis.ExploratoryAnalysis import Visualize
from processing.python.common.FileLocation import File_Location
from processing.python.merger.NoiseGPSMerger import NoiseGPSMerger
from processing.python.merger.E4Downsampler import Downsampler
from processing.python.merger.SensorE4Merger import SensorE4Merger
from multiprocessing import Process
import pandas as pd
import os

class Aggregater:
    def __init__(self, main_dir):
        self.main_dir = main_dir
        self.file_locator = File_Location()

    def aggregate_e4_sensor(self):
        output_results = self.main_dir + "/Results"

        eda_dir_path = self.main_dir + "/EDA"
        downsample = Downsampler(eda_dir_path, output_results)
        downsample.create_E4_pd()

        sensor_dir = self.main_dir + 'kestrel/'
        sensor_file = self.file_locator.get_csv_file(file_dir=sensor_dir)

        scr_file = self.file_locator.get_xls_file(file_dir=eda_dir_path)

        tag_file = eda_dir_path + "/tags_labeled.csv"
        if '.csv' not in sensor_file:
            print "No Sensor File for given user"
        else:
            input_e4 = output_results + "/Merged_EDA.csv"
            merge_other = SensorE4Merger(sensor_file, input_e4, output_results, self.main_dir)
            filter_columns = ['FORMATTED DATE_TIME', 'Station Pressure', 'Wind Speed', 'WBGT', 'Heat Stress Index',
                              'Temperature', 'Relative Humidity']
            datetime_col = 'FORMATTED DATE_TIME'
            pressure_col = 'Station Pressure'
            merge_other.mergeSensorFile(filter_columns, datetime_col, pressure_col)
            merge_other.add_tags(tag_file)

            if '.xls' not in scr_file:
                print "No SCR file for given user"
            else:
                merge_other.addscr_tofile(scr_file)

        print 'Done Merging of Sensor and E4'


    def aggregate_noise_gps(self):
        output_results = self.main_dir + "/Results/"

        gps_dir = self.main_dir + 'GPS/'
        gps_file = self.file_locator.get_csv_file(file_dir=gps_dir)

        photo_gps = '/home/striker/Dropbox/NSE_2018_e4/Experiment/gps_temporal.csv'
        merger = NoiseGPSMerger(photo_gps)
        pd_gps, curr_date = pd.DataFrame(), ""

        if '.csv' not in gps_file:
            print "No GPS File found for the given user"
        else:
            pd_gps, curr_date = merger.get_speed_data(gps_file=gps_file)

        noise_dir = self.main_dir + 'noise/'
        noise_file = self.file_locator.get_csv_file(noise_dir)
        pd_noise = pd.DataFrame()

        if '.csv' not in noise_file:
            print "No Noise File found for the given user"
        else:
            pd_noise = merger.get_noise_data(noise_file=noise_file, date=curr_date)

        if not pd_noise.empty and not pd_gps.empty:
            output_file = output_results + 'GPSNoiseMerge.csv'
            merger.combine(pd_a=pd_gps, pd_b=pd_noise, output_file=output_file)
        elif not pd_gps.empty:
            pd_gps.to_csv(output_results + 'GPSNoiseMerge.csv', index=False)
        else:
            print 'Check if both files are present'

        print 'Done Merging of Noise and GPS'

if __name__ == '__main__':
    main_dir = "/home/striker/Dropbox/NSE_2018_e4/Experiment/"
    # participants = ['2', '3', '4', '5', '6', '7']
    participants = ['7']
    for user in participants:
        print 'Processing Data for user: ' + user
        if not os.path.exists(main_dir + user + '/Results'):
            os.makedirs(main_dir + user + '/Results' )

        gps_file = main_dir + "/GPS/GPS.csv"

        aggregate = Aggregater(main_dir + user + '/')

        # process1 = Process(target=aggregate.aggregate_e4_sensor())
        # process1.start()
        # process2 = Process(target=aggregate.aggregate_noise_gps())
        # process2.start()

        input_dir = main_dir + user + "/Results/"

        for lap in ["Lap 1", "Lap 2"]:
            y1, y2 = "Skin Temp", "Heat_Stress_Index"

            output_file = "Plot_A_" + lap
            # Visualize(input_dir).twoAxisPlot(y1_label=y1, y2_label=y2, lap=lap, output_file=output_file)
            Visualize(input_dir).scatterPlot(lap)
