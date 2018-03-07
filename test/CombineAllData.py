from main.downsampling.MergerEDAEnivronment import Merger
from main.extra.Merger import MergeOtherSensor

if __name__ == '__main__':
    eda_dir_path = "/home/striker/Downloads/Bige"
    input_e4 = eda_dir_path +  "/Merged.csv"
    input_sensor = "/home/striker/Downloads/March_6_945.csv"
    columns = "Readable_Time, EDA, TEMP, HR, Humidity, Temperature, Pressure, Light, IR Temperature, Noise\n"

    merge = Merger(eda_dir_path)
    merge.create_E4_pd()
    merge_other = MergeOtherSensor(input_sensor, input_e4, eda_dir_path)
    merge_other.merger_files(columns)
