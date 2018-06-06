from sklearn.preprocessing import MinMaxScaler
import pandas as pd

from main.models.Features_Selection import Features
from main.models.Regression_Models import Regression_Models
from processing.python.common.FileLoader import FileLoader


class FeatureSelection:

    def __init__(self):
        self.main_dir =  "/home/striker/Dropbox/NSE_2018_e4/Experiment/"
        self.output_dir = "/home/striker/Dropbox/NSE_2018_e4/Experiment/"

    def mergeData(self):
        participants = ['3', '4', '6', '7', '8', '9', '10', '11', '12']

        scaler = MinMaxScaler()
        pd_total = pd.DataFrame()
        for user in participants:
            output_results = self.main_dir + user + "/Results/"
            f = FileLoader(output_results)
            pd_eda, pd_noise = f.filesDataframe()
            pd_photo = f.loadPhotoFile()

            pd_noise = pd_noise.merge(pd_photo, on="Photo_id", how="left")
            pd_eda = pd_eda.merge(pd_noise.rename(columns={'time': 'Epoc_Time'}), how='left')

            pd_eda["SCR"] = pd_eda["SCR"].round(6)
            pd_eda["Residential_comp_10"] = pd_eda["Residential_comp_10"] / 314
            pd_eda["Park_comp_10"] = pd_eda["Park_comp_10"] / 314
            pd_eda["Road_comp_10"] = pd_eda["Road_comp_10"] / 314

            pd_eda = pd_eda[pd_eda['Tags'] != 0]
            pd_eda = pd_eda[pd_eda['Tags'] != 10]
            pd_eda = pd_eda[pd_eda['Tags'] != 20]
            pd_eda = pd_eda[pd_eda['Tags'] != 30]

            pd_eda = pd_eda[pd_eda["Valid"] != 1]

            scaled_pd = scaler.fit_transform(pd_eda[["EDA", "SCR"]])
            pd_eda["EDA"] = scaled_pd[:, 0]
            pd_eda["SCR"] = scaled_pd[:, 1]
            pd_eda = pd_eda.dropna(axis=0)

            pd_eda = pd_eda[
                ["SCR", "Station Pressure", "Wind Speed", "WBGT", "Heat_Stress_Index", "Temperature", "Humidity",
                 "Tags",
                 "Count", "gain", "Speed", "Residential_comp_10", "Park_comp_10", "Road_comp_10", "Clutter", "Sky",
                 "Building", "Tree", "Lap"]]
            pd_total = pd_total.append(pd_eda)

        return pd_total


    def featureImportance(self):
        output_file = self.output_dir + '/Feature_Importance.csv'
        pd_feature = pd.DataFrame()

        pd_total = self.mergeData()
        target = "SCR"
        features = ["Station Pressure", "Wind Speed", "WBGT", "Heat_Stress_Index", "Temperature", "Humidity",
                    "Count", "gain", "Speed", "Residential_comp_10", "Park_comp_10", "Road_comp_10", "Sky", "Clutter"]

        pd_feature = pd_feature.append(pd.DataFrame(features))

        for algo in ['RF', 'LR', 'Ridge', 'SVR']:
            print "Feature generation using model: ", algo

            for lap in ['Lap 1', 'Lap 2']:
                print "Feature Selection for: ", lap
                pd_lap = pd_total[pd_total["Lap"] == lap]

                for section in [11, 12, 13, 14, 21, 22, 23, 24]:
                    pd_section = pd_lap[pd_lap['Tags'] == section]
                    print "Computing for sectionnumber: ", str(section), len(pd_section)

                    if not pd_section.empty:
                        feature = Features(pd_section)
                        importance = feature.RFECV_feature_selection(target=target, features=features, type=algo)
                        new_col = algo + "_" + lap + "_" + str(section)
                        pd_feature[new_col] = importance

        pd_feature.to_csv(output_file, index=False)

if __name__ == '__main__':
    FeatureSelection().featureImportance()

    # regression_model = Regression_Models(pd_total)
    # target = "SCR"
    # features = ["Station Pressure", "Wind Speed", "WBGT", "Heat_Stress_Index", "Temperature", "Humidity", "Tags",
    #             "Count", "gain", "Speed", "Residential_comp_10", "Park_comp_10", "Road_comp_10"]
    # regression_model.linerar_regression(target=target, features=features)
    #
    #
    # feature = Features(pd_total)
    # feature.RFECV_feature_selection(target=target, features=features)