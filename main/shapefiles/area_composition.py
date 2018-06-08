import fiona
from shapely.geometry import shape, Point
import geopandas as gpd


class Intersection:
    def __init__(self, input_file):
        self.input_file = input_file
        self.geoms = []
        self.area_type = []

    def read_shape(self, types):
        for feature in fiona.open(self.input_file):
            if types:
                self.area_type.append(feature['properties']['LU_DESC'])
            else:
                self.area_type.append("Type 1")
            self.geoms.append(shape(feature['geometry']))

    def find_area_type(self, coord):
        pts = Point(coord)
        for poly, area in zip(self.geoms, self.area_type):
            if poly.contains(pts):
                return area
        return 'None'

    def find_intersected_area(self, new_geometry):
        areas = {}
        for polygon, area_type in zip(self.geoms, self.area_type):
            calc_area = polygon.intersection(new_geometry)
            if calc_area.area > 0:
                if str(area_type) in areas:
                    areas[str(area_type)].append(calc_area)
                else:
                    areas[str(area_type)] = [calc_area]
        return areas


class CreateBuffer:
    def __init__(self, coord):
        self.pts = Point(coord)

    def project_point(self, geometry):
        gdf = gpd.GeoDataFrame()
        gdf.crs = {'init': 'epsg:4326'}
        gdf['geometry'] = None
        gdf.loc[0, 'geometry'] = geometry

        utm_crs = {
            'ellps': 'WGS84',
            'proj': 'utm',
            'zone': '48N',
            'units': 'm'
        }
        reprojected_point = gdf.to_crs(utm_crs)
        geometry_proj = reprojected_point['geometry'].iloc[0]

        return geometry_proj, reprojected_point.crs

    def find_buffer_endpoints(self, geometry, to_crs):
        gdf = gpd.GeoDataFrame()
        gdf.crs = to_crs
        gdf['geometry'] = None
        gdf.loc[0, 'geometry'] = geometry
        reprojected_point = gdf.to_crs({'init': 'epsg:4326'})
        geometry_proj = reprojected_point['geometry'].iloc[0]

        return geometry_proj, reprojected_point.crs

    def create_buffer(self, buffere_size):
        geom, geo_proj = self.project_point(self.pts)
        buffer_proj = geom.buffer(buffere_size)
        new_geo, new_proj = self.find_buffer_endpoints(buffer_proj, geo_proj)
        return new_geo



class AreaComposition:

    def __init__(self, pts):
        self.pts = pts

    def get_area_composition(self, buffer_size, file_path):
        file_path = '/home/striker/Dropbox/NSE_2018_e4/Shapes/Tampines_land_use/Tampines_subset_use_of_land.shp'
        intersect = Intersection(file_path)
        intersect.read_shape(True)

        c = CreateBuffer(self.pts)
        new_geo = c.create_buffer(buffere_size=buffer_size) # in meters
        areas = intersect.find_intersected_area(new_geo)

        area_composition = {}
        for key, value in areas.iteritems():
            total_area = 0
            for geom in value:
                geometry_proj, crs = c.project_point(geom)
                total_area += geometry_proj.area

            if key in area_composition:
                area_composition[key] += total_area
            else:
                area_composition[key] = total_area

        return area_composition