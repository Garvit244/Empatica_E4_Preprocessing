import pandas as pd
from sklearn import preprocessing
from sklearn import cluster
import matplotlib.pyplot as plt
import numpy as np
import os


class clusters:
    def __init__(self):
        self.input_data = pd.DataFrame()

    def normalize(self, pd_a):
        pd_a = pd_a.dropna(how='any')
        pd_a = pd_a[pd_a.Tags != 'None']
        pd_a = pd_a[pd_a.Tags != 'Rest']
        pd_a = pd_a[pd_a.Tags != 'End']
        pd_a = pd_a[pd_a.Tags != 'Drop']

        min_max_scalar = preprocessing.MinMaxScaler()

        temp = min_max_scalar.fit_transform(pd_a.iloc[:,6].values)
        humidity = min_max_scalar.fit_transform(pd_a.iloc[:,5].values)
        noise = min_max_scalar.fit_transform(pd_a.iloc[:,10].values)
        light = min_max_scalar.fit_transform(pd_a.iloc[:,8].values)
        pressure = min_max_scalar.fit_transform(pd_a.iloc[:,7].values)
        labels = pd_a.iloc[:, 11].values

        temp_pd = pd.DataFrame([temp, humidity, noise, light, pressure, labels]).T

        self.input_data = self.input_data.append(temp_pd)
        print len(self.input_data)

        return self.input_data

    def k_means_cluster(self, data, no_of_cluster):
        model = cluster.KMeans(n_clusters=no_of_cluster, random_state=0)
        result = model.fit(data)
        return result.labels_

    def plot_k_means(self,x, true, predicted, clusters, output_fig):
        fig = plt.figure(figsize=(20, 12))
        plt.title("K-Means cluster using " + str(clusters))
        plt.plot(x, true, 'b--',label='True Cluster')
        plt.plot(x, predicted, 'r*', label='Predicted Cluster')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        # plt.show()

        plt.savefig(output_fig, dpi=fig.dpi)

c = clusters()
users = ['Francisco']


for user in users:
    print "Processing User: ", user
    directory = '/home/striker/Dropbox/NSE_2018_e4/Tampines/6_April/' + user + '/Results/'
    data = c.normalize(pd.read_csv(directory + 'Data_w_tags_1.csv'))

    no_of_cluster = 2
    true_labels = pd.factorize(data.iloc[:,-1])[0]

    if not os.path.exists(directory + 'Clustering_Result'):
        os.makedirs(directory + 'Clustering_Result' )

    for val in zip([2, 3, 4, 5, 6]):
        predicted_labels = c.k_means_cluster(data.iloc[:, :-1], val[0])
        output_file = directory + 'Clustering_Result'  + '/K-Means_w_cluster_' + str(val[0]) + '.png'

        x_axis =  np.arange(0, len(true_labels), 1)
        c.plot_k_means(x_axis, true_labels, predicted_labels, val[0], output_file)

