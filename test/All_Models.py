import pandas as pd
from sklearn import preprocessing

from main.models.Features_Selection import Features
from main.models.Regression_Models import Regression_Models

if __name__ == '__main__':
    dates = ['16_March', '17_March', '19_March', '20_March']

    pd_total = pd.DataFrame()
    for date_val in dates:
        file_path = '/home/striker/Dropbox/NSE_2018_e4/Simei_Morning_Trips/' + date_val + '/Francisco/Results/Interpolated_Data_w_tags.csv'
        pd_a = pd.read_csv(file_path)
        pd_a = pd_a[pd_a.Tags != 'None']
        pd_a = pd_a[pd_a.Tags != 'Resting']
        pd_a = pd_a[pd_a.Tags != 'End']
        pd_a = pd_a[pd_a.Tags != 'Drop']
        pd_a = pd_a.dropna(axis=0, how='any')

        pd_a = pd_a[pd_a.SCR != 0]
        scr_values = pd_a['SCR'].values
        min_max_scalar = preprocessing.MinMaxScaler()
        scr_scaled = min_max_scalar.fit_transform(scr_values)
        scr_scaled = pd.DataFrame([scr_scaled]).values[0]

        pd_a = pd_a.drop(['SCR'], axis=1)
        pd_a['SCR'] = scr_scaled
        pd_total = pd_total.append(pd_a, ignore_index=True)

    pd_total = pd_total[pd_total.SCR != 0]
    pd_total = pd_total.dropna(subset=['Speed'])

    features = ['Noise', 'Humidity','Temperature', 'Pressure', 'Light', 'IR Temperature',
                              'Segment_Mean_Temp', 'Segment_Std_Temp', 'Segment_Mean_Humi', 'Segment_Std_Humi',
                              'Segment_Mean_Pressure','Segment_Std_Pressure', 'Segment_Mean_Light', 'Segment_Std_Light',
                              'Segment_Mean_Noise', 'Segment_Std_Noise', 'Scr_Per_Segment', 'Speed']


    # regression = Regression_Models(pd_total)
    features_selection = Features(pd_total)
    features_selection.RFECV_feature_selection(target='SCR', features=features)
    # regression.linerar_regression(target='SCR', features=features)