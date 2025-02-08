''' 
    This class provides communicating with TIF file: Geo2Pixel Pixel2Geo
    Made by Andrey Underoak(https://github.com/AndreyUnderoak) & Nancy Underoak(https://github.com/NancyUnderoak)
'''

from osgeo import osr, gdal
import numpy as npy
import matplotlib.pyplot as mplot  
from termcolor import colored
import rasterio

class Img_Geo():
    def __init__(self, link_to_file, link_to_depth = None):
        print(colored("Reading data from odm_orthophoto.tif ...",'yellow'))
        
        self.tif_file = gdal.Open(link_to_file)
        
        # Reading IMG
        self.read_img()        

        # Reading GEO
        self.read_geo_transform(self.tif_file.GetGeoTransform())

        self.get_projections()

        self.depth_arr = None
        if link_to_depth is not None:
            self.depth_arr = rasterio.open(link_to_depth)
            ds = gdal.Open(link_to_depth)
            self.depth_arr = ds.GetRasterBand(1).ReadAsArray()

    def get_pixel_from_geo(self, geo_vector):
        print("\nCalculating pixel from geo...")
        print("Input geo: (" + str(geo_vector[0]) + "; " + str(geo_vector[1]) + ")")
        geo_old_vector = self.transform_from_new.TransformPoint(geo_vector[0],geo_vector[1])
        
        pixel_vector = []
        pixel_vector.append(int((geo_old_vector[0] - self.pixel_x0_geo) / self.pixel_width_geo))
        pixel_vector.append(int((geo_old_vector[1] - self.pixel_y0_geo) / self.pixel_height_geo))
        
        print("Output pixel: (" + str(pixel_vector[0]) + "; " + str(pixel_vector[1]) + ")  +- 1 pixel\n")
        return pixel_vector
    
    def get_geo_from_pixel(self, pixel_vector):
        print("\nCalculating geo from pixel...")
        print("Imput pixel: (" + str(pixel_vector[0]) + "; " + str(pixel_vector[1]) + ")")
        geo_old_vector = []
        geo_old_vector.append(self.pixel_x0_geo + pixel_vector[0] * self.pixel_width_geo  + pixel_vector[1] * self.angle_row_geo)
        geo_old_vector.append(self.pixel_y0_geo + pixel_vector[0] * self.angle_colomn_geo + pixel_vector[1] * self.pixel_height_geo)

        geo_vector = self.transform_to_new.TransformPoint(geo_old_vector[0],geo_old_vector[1]) 
        
        print("Output geo: (" + str(geo_vector[0]) + "; " + str(geo_vector[1]) + ")\n")
        return geo_vector
    
    # x, y from image approved
    def get_depth_from_pic(self, x: int, y: int) -> float:
        if self.depth_arr is None:
            raise ValueError("Нет карты глубины")
        # if not (0 <= x < self.depth_arr.width and 0 <= y < self.depth_arr.height):
        #     raise ValueError(f"Координаты ({x}, {y}) выходят за границы изображения")
        return self.depth_arr[y, x]
    
    def get_depth_from_geo(self, geo_vector):
        if self.depth_arr is None:
            raise ValueError("Нет карты глубины")
        pix_vec = self.get_pixel_from_geo(geo_vector)
        return self.get_depth_from_pic(pix_vec[0], pix_vec[1])
        
    def read_img(self):
        self.img_width  = self.tif_file.RasterXSize
        self.img_height = self.tif_file.RasterYSize

        self.print_img_info()

        # Converting to png
        print("\nConverting to print:")
        layers = []
        for i in range(3):
            print(str(i) + " layer")
            layers.append(self.tif_file.GetRasterBand(i+1).ReadAsArray())
        
        self.img = npy.dstack((layers[0], layers[1], layers[2]))  
        
    def read_geo_transform(self,tiff_transform_data):
        self.pixel_x0_geo     = tiff_transform_data[0]
        self.pixel_y0_geo     = tiff_transform_data[3]
        self.pixel_width_geo  = tiff_transform_data[1]
        self.pixel_height_geo = tiff_transform_data[5]
        self.angle_row_geo    = tiff_transform_data[2]
        self.angle_colomn_geo = tiff_transform_data[4]

        self.print_geo_transform_info()

    def get_projections(self):
        # get the existing coordinate system
        old_cs= osr.SpatialReference()
        old_cs.ImportFromWkt(self.tif_file.GetProjectionRef())

        print("\nGet transform of projection ...")
        # create the new coordinate system
        wgs84_wkt = """
        GEOGCS["WGS 84",
            DATUM["WGS_1984",
                SPHEROID["WGS 84",6378137,298.257223563,
                    AUTHORITY["EPSG","7030"]],
                AUTHORITY["EPSG","6326"]],
            PRIMEM["Greenwich",0,
                AUTHORITY["EPSG","8901"]],
            UNIT["degree",0.01745329251994328,
                AUTHORITY["EPSG","9122"]],
            AUTHORITY["EPSG","4326"]]"""
        new_cs = osr.SpatialReference()
        new_cs.ImportFromWkt(wgs84_wkt)
        # print("\nNew Projection: " + str(new_cs))

        # create a transform object to convert between coordinate systems
        self.transform_to_new   = osr.CoordinateTransformation(old_cs,new_cs) 
        self.transform_from_new = osr.CoordinateTransformation(new_cs,old_cs) 

    def save_png(self):
        f = mplot.figure()  
        mplot.imshow(self.img)
        mplot.savefig('Tiff.png')  

    def print_img_info(self):
        print(colored("\nImage INFO:",'green'))
        print("widht  = " + str(self.img_width))
        print("height = " + str(self.img_height))

    def print_geo_transform_info(self):
        print(colored("\nGeo INFO:",'green'))
        print("x0 pixel coordinate = " + str(self.pixel_x0_geo))
        print("y0 pixel coordinate = " + str(self.pixel_y0_geo))
        print("pixel width         = " + str(self.pixel_width_geo))
        print("pixel height        = " + str(self.pixel_height_geo))
        print("row angle           = " + str(self.angle_row_geo))
        print("colomn angle        = " + str(self.angle_colomn_geo))

    def get_img(self):
        return self.img
        

