''' 
    This script provides depth info from tiff
    Made by Andrey Underoak(https://github.com/AndreyUnderoak)
'''
from classes.Img_Geo import Img_Geo
from termcolor import colored
import sys
import pandas as pd
import cv2

def read_xlsx(file_path):
    df = pd.read_excel(file_path, usecols=[0, 1], engine='openpyxl')
    
    for index, row in df.iterrows():
        x, y = row[0], row[1]
        print(f"Row {index + 1}: x = {x}, y = {y}")
        yield x, y

if(len(sys.argv) < 4):
    print(colored("Please write: python3 depth_getter.py <path/map.tif> <path/depth.tif> <xlsx file>",'red'))
    exit()

tiff_path   = str(sys.argv[1])
depth_path  = str(sys.argv[2])
xlsx_path   = str(sys.argv[3])

tiff        = Img_Geo(tiff_path, depth_path)

tiff_img    = cv2.imread(tiff_path, cv2.IMREAD_COLOR)

cv2.namedWindow("Display", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Display", 1920, 1080)

# print(tiff.get_depth_from_pic(500,2128))
# /\/\/\/\/CALCULATING DELTA\/\/\/\/\/
px_coors = tiff.get_geo_from_pixel([500,2128])
cv2.circle(tiff_img,(505,2128), 20, (0,255,0), -1)
px_coors2 = tiff.get_geo_from_pixel([450,2128])
cv2.circle(tiff_img,(450,2128), 20, (0,255,0), -1)

d_x = px_coors[0] - px_coors2[0]
d_y = px_coors[1] - px_coors2[1]

# print(px_coors2[0], d_x)
# new_px_coors = [px_coors2[0], px_coors2[1] + d_y]
# new_px = tiff.get_pixel_from_geo(new_px_coors)
# print("NEW PX: ", new_px)
# cv2.circle(tiff_img,(new_px[0],new_px[1]), 10, (255,0,0), -1)
# print("depth on delta: ", tiff.get_depth_from_pic(new_px[0], new_px[1]))

print("deltas: ", d_x, d_y)
# /\/\/\/\/END CALCULATING DELTA\/\/\/\/\/


# print(tiff.get_depth_from_geo(tiff.get_geo_from_pixel([5000,11000])))

# for x, y in read_xlsx(xlsx_path):
#     try:
#         pix_coors = tiff.get_pixel_from_geo([x, y + d_y])
#         cv2.circle(tiff_img,(pix_coors[0],pix_coors[1]), 30, (0,0,255), -1)
#         print("depth: ", tiff.get_depth_from_pic(pix_coors[0], pix_coors[1])) 
#     except:
#         pass

while(True):
    cv2.imshow("Display", tiff_img)
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    else: 
        continue


    


