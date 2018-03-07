import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Merger:
    def __init__(self, eda_dir_path):
        self.eda_dir_path = eda_dir_path

    def convert_date(self, epoc_time, time_zone):
        value = datetime.fromtimestamp(epoc_time)
        value = value - timedelta(hours=time_zone)
        time_s = value.strftime('%H:%M:%S')
        return time_s

    def create_E4_pd(self):
        pd_EDA = pd.read_csv(self.eda_dir_path + '/EDA.csv', header=None)
        pd_TEMP = pd.read_csv(self.eda_dir_path + '/TEMP.csv', header=None)
        pd_HR = pd.read_csv(self.eda_dir_path + '/HR.csv', header=None)

        merged_data = open(self.eda_dir_path + '/Merged.csv', 'w')
        merged_data.write('Epoc_Time, Readable_Time, EDA, TEMP, HR\n')

        EDA_start_time = int(pd_EDA.iloc[0].values[0])
        HR_start_time = int(pd_HR.iloc[0].values[0])

        EDA_sampling = pd_EDA.iloc[1].values[0]
        TEMP_sampling = pd_TEMP.iloc[1].values[0]

        pd_EDA = pd_EDA[2:]
        pd_TEMP = pd_TEMP[2:]
        pd_HR = pd_HR[2:]

        EDA_count = len(pd_EDA)
        TEMP_count = len(pd_TEMP)

        pd_TEMP = pd_TEMP.groupby(np.arange(TEMP_count) // TEMP_sampling).mean()
        pd_EDA = pd_EDA.groupby(np.arange(EDA_count) // EDA_sampling).mean()
        combine_EDA_TEMP = pd.concat([pd_EDA, pd_TEMP], axis=1)

        if HR_start_time != EDA_start_time:
            time_difference = HR_start_time - EDA_start_time
            combine_EDA_TEMP = combine_EDA_TEMP[time_difference-1:]

        pd_time = pd.DataFrame(range(HR_start_time, HR_start_time + len(pd_HR), 1))

        for index in range(0, len(pd_HR)):
            EDA_TEMP = combine_EDA_TEMP.iloc[index].values
            HR = pd_HR.iloc[index].values[0]
            epoc_time = pd_time.iloc[index].values[0]
            readable_time = self.convert_date(epoc_time, time_zone=0)

            merged_data.write(str(epoc_time) + ',' + str(readable_time) + ',' + str(EDA_TEMP[0]) + ',' + str(EDA_TEMP[1]) + ',' + str(HR) + '\n')


    def filtered_data(self):
        pd_merged = pd.read_csv(self.eda_dir_path + '/Merged.csv')
        pd_merged.columns = ["Epoc", "Time", "EDA", "TEMP", "HR"]
        print "Actual Data with Noise ", len(pd_merged)
        pd_noise = pd.read_csv(self.eda_dir_path + '/noise.csv')
        pd_filtered = pd.DataFrame()

        filtered_data = pd_noise.loc[pd_noise['BinaryLabels'] == 1]
        print "Filtered Data with Lables equal to 1 ", len(filtered_data)

        for index, row in filtered_data.iterrows():
            start_time = int(datetime.strptime(str(row['StartTime']), '%Y-%m-%d %H:%M:%S').strftime('%s'))
            end_time = int(datetime.strptime(str(row['EndTime']), '%Y-%m-%d %H:%M:%S').strftime('%s'))
            start_time += 8 * 60 * 60
            end_time += 8 * 60 * 60

            filtered_pd = pd_merged.loc[(pd_merged["Epoc"] >= start_time) & (pd_merged["Epoc"] <= end_time)]
            pd_filtered = pd.concat([pd_filtered, filtered_pd])

        pd_filtered = pd_filtered.drop_duplicates()
        print 'Total EDA Values ', len(pd_filtered)

        pd_filtered.to_csv(self.eda_dir_path + '/Filtered_data.csv')
        pd_filtered.to_csv(self.eda_dir_path + '/Filtered_EDA.csv', columns=['EDA'], header=None, index=False)
        pd_filtered.to_csv(self.eda_dir_path + '/Filtered_TEMP.csv', columns=['TEMP'], header=None, index=False)

if __name__ == '__main__':
    eda_dir_path = "/home/striker/Downloads/Francisco"

    merge = Merger(eda_dir_path)
    merge.create_E4_pd()
