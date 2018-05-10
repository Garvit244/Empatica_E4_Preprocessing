import pandas as pd

class NoiseGPSMerger:

    def get_speed_data(self, gps_file):
        pd_gps = pd.read_csv(gps_file)
        pd_gps = pd_gps[['Time', 'Speed', 'Lat', 'Lng']]
        curr_date = pd.to_datetime(pd_gps['Time']).dt.date[0]
        pd_gps['Time'] = pd.DataFrame(pd.to_datetime(pd_gps['Time']).view('int64') / pow(10, 9)).astype('int')
        pd_gps['Time'] += 8*60*60  # Time is in GMT
        return pd_gps, curr_date

    def get_noise_data(self, noise_file, date):
        pd_noise = pd.read_csv(noise_file)
        pd_noise['time'] = pd.DataFrame(pd_noise['time'].str[:-4])
        pd_noise['time'] = pd.DataFrame(pd.to_datetime(str(date) + ' ' + pd_noise['time'].astype('str')).view('int64')
                                        / pow(10, 9)).astype('int')
        pd_noise =  pd_noise.groupby('time', as_index=False).mean()
        return pd_noise

    def combine(self, pd_a, pd_b, output_file):
        pd_new = pd_b.merge(pd_a.rename(columns={'Time': 'time'}), how='left')
        pd_new = pd_new.fillna(method='ffill')
        pd_new.to_csv(output_file, index=False)
