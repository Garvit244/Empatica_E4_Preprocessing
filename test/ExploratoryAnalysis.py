from main.EDA.Annova import Annova
import pandas as pd
import numpy as np
import os

if __name__ == '__main__':
    source_dir = '/home/striker/Dropbox/NSE_2018_e4/Tampines/6_April/Results/'
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)

    users = ['Francisco', 'Garvit', 'Sarah', 'Iman', 'Francesco', 'Darshan']

    pd_total = pd.DataFrame()
    pd_participant = pd.DataFrame()
    pd_kruskal = pd.DataFrame()

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

        file_path = directory + 'Interpolated_Data_w_tags_' + str(file_to_use) + '.csv'
        output_results = directory + 'Figures/'

        if not os.path.exists(output_results):
            os.makedirs(output_results)

        pd_a = pd.read_csv(file_path)
        pd_a = pd_a.iloc[:, 5:12]
        pd_a = pd_a[pd_a.Tags != 'None']
        pd_a = pd_a[pd_a.Tags != 'Rest']
        pd_a = pd_a[pd_a.Tags != 'End']
        pd_a = pd_a[pd_a.Tags != 'Drop']
        pd_a = pd_a.dropna(axis =0, how='any')

        pd_total = pd_total.append(pd_a, ignore_index=True)

        print pd_total.isnull().any()
        print '\n'
        pd_total = pd_total.dropna(axis=1, how='any')

        annova_dict = []
        kruskal_list = []
        annova_dict.append(user)
        kruskal_list.append(user)

        variables = ['Noise', 'Humidity','Temperature', 'Pressure', 'Light', 'IR Temperature']
        for variable in variables:
            annova = Annova(pd_a, output_results)
            p, kp = annova.anova(variable, 'Tags')
            annova.plot(variable, 'Tags')
            annova_dict.append(str(p))
            kruskal_list.append(str(kp))

        new_pd = pd.DataFrame(np.array(annova_dict).reshape(1,7), columns=['User', 'Noise', 'Humidity','Temperature', 'Pressure',
                                                     'Light', 'IR Temperature'])

        pd_participant = pd_participant.append(new_pd)
        new_pd = pd.DataFrame(np.array(kruskal_list).reshape(1, 7),
                              columns=['User', 'Noise', 'Humidity', 'Temperature', 'Pressure',
                                       'Light', 'IR Temperature'])

        pd_kruskal = pd_kruskal.append(new_pd)

    annova_dict = []
    annova_dict.append('Total')

    variables = ['Noise', 'Humidity', 'Temperature', 'Pressure', 'Light', 'IR Temperature']
    for variable in variables:
        annova = Annova(pd_total, source_dir)
        p, kp = annova.anova(variable, 'Tags')
        annova.plot(variable, 'Tags')
        annova_dict.append(str(p))

    new_pd = pd.DataFrame(np.array(annova_dict).reshape(1, 7),
                          columns=['User', 'Noise', 'Humidity', 'Temperature', 'Pressure',
                                   'Light', 'IR Temperature'])
    pd_participant = pd_participant.append(new_pd)

    kruskal_list = []
    kruskal_list.append('Total')

    variables = ['Noise', 'Humidity', 'Temperature', 'Pressure', 'Light', 'IR Temperature']
    for variable in variables:
        annova = Annova(pd_total, source_dir)
        p, kp = annova.anova(variable, 'Tags')
        kruskal_list.append(str(p))

    new_pd = pd.DataFrame(np.array(kruskal_list).reshape(1, 7),
                          columns=['User', 'Noise', 'Humidity', 'Temperature', 'Pressure',
                                   'Light', 'IR Temperature'])
    pd_kruskal = pd_kruskal.append(new_pd)

    pd_participant.to_csv(source_dir + 'Annova.csv', index=False)
    pd_kruskal.to_csv(source_dir + 'Kruskal.csv', index=False)
