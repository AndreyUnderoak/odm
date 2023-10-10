''' 
    This script provides drone visualisation on map from ODM by coordinates from ros topic
    Made by Andrey Underoak(https://github.com/AndreyUnderoak) & Nancy Underoak(https://github.com/NancyUnderoak)
'''

from classes.Topic_reader import Topic_reader, TopicException
from classes.Img_Geo import Img_Geo
from termcolor import colored
import cvzone
import cv2 
import sys

  

drone_width  = 254


if(len(sys.argv) < 4):
    print(colored("Please write path to .tif map and .png drone image: python3 continious_printer.py <coordinates topic> <path/map.tif> <path/drone.png> (optional)<drone width in px>",'red'))
    exit()

topic      = sys.argv[1]
tiff_path  = str(sys.argv[2])
drone_path = str(sys.argv[3])
    
drone_width  = 254
if(len(sys.argv) == 5):
    drone_width = int(sys.argv[4])
drone_height = drone_width

tiff         = Img_Geo(tiff_path)
topic_reader = Topic_reader(topic)

print(colored("Reading png images..", 'yellow'))
tiff_img = cv2.imread(tiff_path, cv2.IMREAD_COLOR)
drone_img = cv2.imread(drone_path, cv2.IMREAD_UNCHANGED)

drone_img = cv2.resize(drone_img, [drone_width,drone_height])

cv2.namedWindow("Display", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Display", 1920, 1080)

i = 0
rotation = 0

class OutOfRangeExeption(Exception):
    def __init__(self):
        print(colored("Drone coordinates OUT OF IMAGE",'red'))
        
def make_image(tiff_img, drone_img_copy, pixel_vector):
    try:
        return cvzone.overlayPNG(tiff_img, drone_img_copy, pixel_vector)
    except:
        raise OutOfRangeExeption()
  

def get_pix_rotation():
    # #--------FOR TEST----------
    # global i
    # global rotation
    # i+=10
    # coordinates = tiff.get_geo_from_pixel([i+1000,4000-i])
    # #--------END TEST----------
    coordinates = topic_reader.get_latest_coor()
    pixel_vector = tiff.get_pixel_from_geo(coordinates)
    # rotation += 10 
    res = [pixel_vector[0], pixel_vector[1], 0]
    print("Recieved: " + str(res))
    return res

#values for centering
delta_width  = int(drone_width/2)
delta_height = int(drone_height/2)

#initial position
geo_init     = [delta_width, delta_height, 0]
geo_rotation = geo_init

while True:
    try:
        drone_img_copy = cvzone.rotateImage(drone_img, geo_rotation[2])
        result = make_image(tiff_img, drone_img_copy, [geo_rotation[0] - delta_width, geo_rotation[1] - delta_height])
        geo_rotation = get_pix_rotation()
    except OutOfRangeExeption:
        geo_rotation = geo_init
    except TopicException:
        geo_rotation = geo_init
        
    cv2.imshow("Display", result)
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    else: 
        continue
    


