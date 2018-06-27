from sklearn.preprocessing import MinMaxScaler
import pandas as pd

from main.models.Features_Selection import Features
from main.models.Regression_Models import Regression_Models
from main.visualization import visualize_feature
from processing.python.common.FileLoader import FileLoader


class FeatureSelection:

    def __init__(self):
        self.main_dir =  "/home/striker/Dropbox/NSE_2018_e4/Experiment/"
        self.output_dir = "/home/striker/Dropbox/NSE_2018_e4/Experiment/"
        self.personal_char = "/home/striker/Dropbox/NSE_2018_e4/00 - Paper/Data_sets/Personal_characteristics.csv"

    def mergeData(self, target):
        participants = ['2', '3', '4', '6', '7', '8', '9', '10', '11', '12']
        pd_personal = pd.read_csv(self.personal_char)

        scaler = MinMaxScaler()
        pd_total = pd.DataFrame()

        for user in participants:
            output_results = self.main_dir + user + "/Results/"
            f = FileLoader(output_results)
            pd_eda, pd_noise = f.filesDataframe()
            pd_photo = f.loadPhotoFile()

            pd_noise = pd_noise.merge(pd_photo, on="Photo_id", how="left")
            pd_eda = pd_eda.merge(pd_noise.rename(columns={'time': 'Epoc_Time'}), how='left')
            pd_eda['participant'] = int(user)

            pd_eda = pd_eda.merge(pd_personal, on='participant', how='left')
            pd_eda[target] = pd_eda[target].round(6)

            pd_eda["Residential_comp_10"] = pd_eda["Residential_comp_10"] / 314
            pd_eda["Park_comp_10"] = pd_eda["Park_comp_10"] / 314
            pd_eda["Road_comp_10"] = pd_eda["Road_comp_10"] / 314

            pd_eda = pd_eda[pd_eda['Tags'] != 0]
            pd_eda = pd_eda[pd_eda['Tags'] != 10]
            pd_eda = pd_eda[pd_eda['Tags'] != 20]
            pd_eda = pd_eda[pd_eda['Tags'] != 30]

            pd_eda = pd_eda[pd_eda["Valid"] != 1]

            # scaled_pd = scaler.fit_transform(pd_eda[["EDA", "SCR"]])
            # pd_eda["EDA"] = scaled_pd[:, 0]
            # pd_eda["SCR"] = scaled_pd[:, 1]
            pd_eda = pd_eda.dropna(axis=0)

            pd_eda['live_in_HDB'] = pd_eda['live_in_HDB'].map( {'Yes': 1, 'No': 0})
            pd_eda['first_time_tampines'] = pd_eda['first_time_tampines'].map( {'Yes': 1, 'No': 0})
            pd_eda = pd_eda[
                [target, "Station Pressure", "Wind Speed", "WBGT", "Heat_Stress_Index", "Temperature", "Humidity",
                 "Tags",
                 "Count", "gain", "Speed", "Residential_comp_10", "Park_comp_10", "Road_comp_10", "Buildings_comp_10",
                 "Clutter", "Sky", "Building", "Tree", "Lap", "participant", "BMI", "live_in_HDB", "PRS_being_away", "PRS_fascination",
                 "PRS_compatibility", "first_time_tampines"]]
            pd_total = pd_total.append(pd_eda)

        return pd_total


    def featureImportance(self, target, sections, filename):
        output_file = self.output_dir + filename + target + '.csv'
        pd_feature = pd.DataFrame()

        pd_total = self.mergeData(target)
        target = target
        features = ["Temperature", "Humidity", "Heat_Stress_Index", "WBGT", "Wind Speed", "gain", "Sky", "Tree",
                    "Buildings_comp_10", "Speed",
                    "PRS_being_away", "PRS_fascination", "PRS_compatibility", "live_in_HDB", "first_time_tampines"]

        column_name = ["Temperature", "Humidity", "Heat Stress Index", "WBGT", "Wind Speed", "Noise", "Sky View Factor", "Green spaces"
                       , "Built-up area", "Walking speed",
                    "PRS being away", "PRS fascination", "PRS compatibility", "Living in HDB", "Familirity"]

        pd_feature = pd_feature.append(pd.DataFrame(column_name))
        for algo in ['RF', 'LR', 'Ridge', 'Lasso']:
            print "Feature generation using model: ", algo

            for lap in ['Lap_1_And_Lap_2']:
                print "Feature Selection for: ", lap
                pd_lap = pd_total

                for section in sections:
                    pd_section = pd_lap.loc[(pd_lap['Tags'] == section[0]) | (pd_lap['Tags'] == section[1])]

                    print "Computing for sectionnumber: ", str(section), len(pd_section)

                    if not pd_section.empty:
                        feature = Features(pd_section)
                        importance = feature.RFECV_feature_selection(target=target, features=features, type=algo)
                        new_col = algo + "_" + lap + "_" + str(section)
                        pd_feature[new_col] = importance

        pd_feature.to_csv(output_file, index=False)
        self.visualizeFeatures(pd_feature, sections=sections, target=target, filename=filename)

    def visualizeFeatures(self, pd_A, sections, target, filename):
        output_file = self.output_dir + filename + target

        for lap in ['Lap_1_And_Lap_2']:
            new_output_file = output_file + '_' + lap + '.png'
            visualize_feature().heatmap(pd_A, segments=sections, output_file=new_output_file, lap=lap)

if __name__ == '__main__':
    sections = [(11, 21), (12, 22), (13, 23), (14, 24)]
    FeatureSelection().featureImportance(target="SCR", sections=sections, filename='Feature_Importance_combine_')