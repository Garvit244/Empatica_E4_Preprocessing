from main.EDA.Annova import Annova
import pandas as pd

if __name__ == '__main__':
    dates = ['16_March', '17_March', '19_March', '20_March']

    pd_total = pd.DataFrame()
    for date_val in dates:
        file_path = '/home/striker/Dropbox/NSE_2018_e4/Simei_Morning_Trips/' + date_val + '/Francisco/Results/Interpolated_Data_w_tags.csv'
        pd_a = pd.read_csv(file_path)
        pd_a = pd_a.iloc[:, 5:12]
        pd_a = pd_a[pd_a.Tags != 'None']
        pd_a = pd_a[pd_a.Tags != 'Resting']
        pd_a = pd_a[pd_a.Tags != 'End']
        pd_a = pd_a[pd_a.Tags != 'Drop']
        pd_a = pd_a.dropna(axis =0, how='any')

        pd_total = pd_total.append(pd_a, ignore_index=True)

    print pd_total.isnull().any()
    print '\n'
    pd_total = pd_total.dropna(axis=1, how='any')


    variables = ['Noise', 'Humidity','Temperature', 'Pressure', 'Light', 'IR Temperature']
    for variable in variables:
        annova = Annova(pd_total)
        annova.anova(variable, 'Tags')
        annova.plot(variable, 'Tags')
