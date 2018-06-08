import pandas as pd
from haversine import haversine
from main.shapefiles.area_composition import AreaComposition

class NoiseGPSMerger:
    def __init__(self, gps_photo_map):
        self.gps_photo_map = gps_photo_map

    def removeMinutes(self, pd_a, minutes):
        return pd_a - pd.Timedelta(minutes=minutes)


    def get_speed_data(self, gps_file, minutes):
        pd_gps = self.add_photo_id_locationwise(gps_file)
        curr_date = pd.to_datetime(pd_gps['Time']).dt.date[0]
        pd_gps['Time'] = pd.DataFrame(self.removeMinutes(pd.to_datetime(pd_gps['Time']), minutes).view('int64') /
                                      pow(10, 9)).astype('int')
        pd_gps['Time'] += 8*60*60  # Time is in GMT
        return pd_gps, curr_date


    def get_noise_data(self, noise_file, date, strip):
        pd_noise = pd.read_csv(noise_file)
        if strip:
            pd_noise['time'] = pd.DataFrame(pd_noise['time'].str[:-4])
        else:
            pd_noise['time'] = pd.DataFrame(pd_noise['time'])

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
                distance_map[haversine(gps_cord, photo_cord)] = photo_id + 1

            pd_gps['Photo_id'].iloc[index] = sorted(distance_map.items())[0][1]

        pd_gps = self.add_area_composition(pd_gps)
        return pd_gps


    def add_area_composition(self, pd_A):
        residential = []
        park = []
        road = []
        buildings = []
        file_path =  '/home/striker/Dropbox/NSE_2018_e4/Shapes/Tampines_land_use/Tampines_subset_use_of_land.shp'
        building_file = '/home/striker/Dropbox/NSE_2018_e4/Shapes/Buildings/buildings_vector1.shp'

        for buffer in [10, 20]:
            for index, row in pd_A.iterrows():
                area = AreaComposition((row['Lng'], row['Lat']))
                composition = area.get_area_composition(buffer_size=buffer, file_path=file_path)

                if 'ROAD' in composition:
                    road.append(composition['ROAD'])
                else:
                    road.append(0)

                if 'RESIDENTIAL' in composition:
                    residential.append(composition['RESIDENTIAL'])
                else:
                    residential.append(0)

                if 'PARK' in composition:
                    park.append(composition['PARK'])
                else:
                    park.append(0)

                building = area.get_area_composition(buffer_size=buffer, file_path=building_file)

                if 'Type 1' in building:
                    buildings.append(building['Type 1'])
                else:
                    buildings.append(0)

            pd_A['Residential_comp_' + str(buffer)] = pd.DataFrame([residential]).T
            pd_A['Park_comp_' + str(buffer)] = pd.DataFrame([park]).T
            pd_A['Road_comp_' + str(buffer)] = pd.DataFrame([road]).T
            pd_A['Buildings_comp_' + str(buffer)] = pd.DataFrame([buildings]).T

            del residential[:]
            del park[:]
            del road[:]
            del  buildings[:]

        return pd_A

