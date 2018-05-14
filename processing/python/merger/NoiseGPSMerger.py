import pandas as pd
from haversine import haversine

class NoiseGPSMerger:
    def __init__(self, gps_photo_map):
        self.gps_photo_map = gps_photo_map

    def get_speed_data(self, gps_file):
        pd_gps = self.add_photo_id_locationwise(gps_file)
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

    def add_photo_id_locationwise(self, gps_file):
        pd_gps = pd.read_csv(gps_file)
        pd_phtoto = pd.read_csv(self.gps_photo_map)

        pd_gps = pd_gps[['Time', 'Speed', 'Lat', 'Lng']]
        pd_gps['Photo_id'] = 0
        for index, gps_data in pd_gps.iterrows():
            distance_map = {}

            for photo_id, photo in pd_phtoto.iterrows():
                photo_cord = (photo[1], photo[2])
                gps_cord = (gps_data[2], gps_data[3])
                distance_map[haversine(gps_cord, photo_cord)] = photo_id

            pd_gps['Photo_id'].iloc[index] = sorted(distance_map.items())[0][1]
        return pd_gps
