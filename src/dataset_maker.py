''' 
    This script provides making dataset for ODM from ROS TOPIC
    Made by Andrey Underoak(https://github.com/AndreyUnderoak) & Nancy Underoak(https://github.com/NancyUnderoak)
'''

from classes.Topic_reader import Topic_reader, TopicException
from classes.Meta_saver   import Meta_saver, MetaException
import cv2
import sys
import time
from termcolor import colored

if(len(sys.argv) < 4):
    print(colored("Please write topic: python3 dataset_maker <files_name> <geo_topic> <image_topic> <auto/none>",'red'))
    exit()
file_name = sys.argv[1]
geo_topic = sys.argv[2]
print(colored(str("subscribing to geo topic:   " + geo_topic),"green"))
img_topic = sys.argv[3]
print(colored(str("subscribing to image topic: " + img_topic),"green"))
topic_reader = Topic_reader(geo_topic, img_topic)

auto = False
if(len(sys.argv) == 5):
    if(sys.argv[4] == "auto"):
        print(colored("AUTO MOD Enabled","green"))
        auto = True

if not auto:
    cv2.namedWindow("Display", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Display", 1920, 1080)
else:
    print(colored("You do not activate auto mod. To take image press 'e', or 'q' to exit","green"))
    print(colored("if you want to activate auto mod: restart programm and type 'auto' in the end of the line","yellow"))

image_num = 0
def save_image(deg, img):
    global image_num
    global file_name
    file_compiled = str(str(file_name) + "_" + str(image_num)+".JPG")
    Meta_saver.save_JPEG_with_meta(file_compiled, deg, img)
    print(colored(str("image saved : " + file_compiled),"green"))
    image_num+=1

while True:
    try:
        #reading the geo from topic in degrees
        deg = topic_reader.get_latest_coor_deg()
        #reading the image from topic in cv2
        img = topic_reader.get_latest_image()
    
    
        if auto:
            save_image(deg, img)
            time.sleep(1)
            continue
        
        #printing the image
        cv2.imshow("Display", img)
        
        #stop if 'q' save if 'e'
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(25) & 0xFF == ord('e'):
            save_image(deg, img)
        else: 
            continue
    
    except TopicException:
        continue
    except MetaException:
        continue