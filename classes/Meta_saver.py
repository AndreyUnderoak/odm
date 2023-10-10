''' 
    This class provides saving JPEG images with geo data for ODM dataset
    Made by Andrey Underoak(https://github.com/AndreyUnderoak) & Nancy Underoak(https://github.com/NancyUnderoak)
'''

import cv2
import piexif
from fractions import Fraction
import os

class Meta_saver:
    
    def to_rat_tuple(number):
        """convert a number to rantional
        Keyword arguments: number
        return: tuple like (1, 2), (numerator, denominator)
        """
        f = Fraction(str(number))
        return (f.numerator, f.denominator)

    def set_meta(self, file_name, geo):
        latitude  = geo[0]
        longitude = geo[1]
        altitude  = geo[2]
        
        exiv_lat = (self.to_rat_tuple(latitude[0]), self.to_rat_tuple(latitude[1]), self.to_rat_tuple(latitude[2]))
        exiv_lng = (self.to_rat_tuple(longitude[0]), self.to_rat_tuple(longitude[1]), self.to_rat_tuple(longitude[2]))
        exiv_alt = self.to_rat_tuple(round(altitude))
        
        gps_ifd = {
            piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
            piexif.GPSIFD.GPSAltitudeRef: 1,
            piexif.GPSIFD.GPSAltitude: exiv_alt,
            piexif.GPSIFD.GPSLatitudeRef: latitude[3],
            piexif.GPSIFD.GPSLatitude: exiv_lat,
            piexif.GPSIFD.GPSLongitudeRef: longitude[3],
            piexif.GPSIFD.GPSLongitude: exiv_lng,
        }
        
        exif_dict = {"GPS": gps_ifd}
        try:
            exif_bytes = piexif.dump(exif_dict)
        except:
            raise MetaException()
        piexif.insert(exif_bytes, file_name)
        
    def save_image(file_name, image):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        cv2.imwrite(file_name, image)
        
    def save_JPEG_with_meta(file_name, geo, image):
        Meta_saver.save_image(file_name, image)
        Meta_saver.set_meta(Meta_saver, file_name, geo)
        
class MetaException(Exception):
    def __init__(self):
        print("Can not put Geo Meta into JPEG image, maybe altitude too low")