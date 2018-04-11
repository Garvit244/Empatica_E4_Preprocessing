import pandas as pd
from main.visualization import visualize_feature
import matplotlib.pyplot as plt

def visualize_scr_per_segment(file_path):
    pd_a = pd.read_csv(file_path)
    print pd_a.groupby(['Tags']).size()
    tags = pd_a.Tags.unique()
    tag_list = []
    value_list = []
    for tag in tags:
        tag_list.append(tag)
        print tag + " " + str(pd_a[pd_a['Tags'] == tag]['Scr_Per_Segment'].values[0])
        value_list.append(str(pd_a[pd_a['Tags'] == tag]['Scr_Per_Segment'].values[0]))

    visualization_feature = visualize_feature()
    visualization_feature.plot_bar_x(tag_list, value_list)

if __name__ == '__main__':
    file_path = '/home/striker/Dropbox/NSE_2018_e4/Simei_Morning_Trips/19_March/Francisco/Results/Interpolated_Data_w_tags.csv'
    # visualize_scr_per_segment(file_path)
    fig, ax = plt.subplots(figsize=(15, 7))
    data = pd.read_csv('/home/striker/Downloads/HealthySubjectsBiosignalsDataSet/Subject1/Subject1AccTempEDA.csv')

    data = data[['EDA', 'Label']]
    print data['Label'].unique()
    data.groupby('Label').plot(kind='kde', ax=ax, label=data['Label'])
    plt.show()