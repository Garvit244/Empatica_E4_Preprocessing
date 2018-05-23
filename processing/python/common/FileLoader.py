import pandas as pd

class FileLoader:
    def __init__(self, input_dir):
        self.input_dir = input_dir

    def filesDataframe(self):
        pd_eda = pd.read_csv(self.input_dir + "Merged_EDA.csv")
        pd_eda.columns = ["Epoc_Time",
                        "Readable_Time",
                        "EDA",
                        "Skin Temp",
                        "HR",
                        "Station Pressure",
                        "Wind Speed",
                        "WBGT",
                        "Heat_Stress_Index",
                        "Temperature",
                        "Humidity",
                        "Tags",
                        "Lap",
                        "SCR",
                        "Count"]

        pd_gps = pd.read_csv(self.input_dir + "GPSNoiseMerge.csv")

        return pd_eda, pd_gps


    def loadPhotoFile(self):
        pd_photo = pd.read_csv("/home/striker/Dropbox/NSE_2018_e4/Experiment/gps_temporal.csv")
        pd_photo.columns = ["Photo_id", "lat", "lon", "Clutter", "Sky", "Building","Tree"]
        return pd_photo