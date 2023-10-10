''' 
    This class provides reading the ros geo and image topics
    Made by Andrey Underoak(https://github.com/AndreyUnderoak) & Nancy Underoak(https://github.com/NancyUnderoak)
'''

import rospy
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class Topic_reader():
    
    bridge = CvBridge()
    location_set = [["S", "N"], ["W", "E"]]
    is_img_sub = False
   
    def __init__(self, coor_topic,img_topic = ""):
        rospy.init_node('listener', anonymous=True)
        self.coor_subscriber = rospy.Subscriber(coor_topic, NavSatFix, self.coor_callback, queue_size=1)
        if(img_topic!=""):
            self.is_img_sub = True
            self.coor_subscriber = rospy.Subscriber(img_topic, Image, self.image_callback, queue_size=1)
        
        self.coor_latest_message = 0
        self.image_latest_message = 0

    def coor_callback(self, message):
        self.coor_latest_message = [message.latitude, message.longitude, message.altitude]
    
    def image_callback(self, message):
        self.image_latest_message = message
   
    def to_deg(self, value, loc):
        """convert decimal coordinates into degrees, munutes and seconds tuple
        Keyword arguments: value is float gps-value, loc is direction list ["S", "N"] or ["W", "E"]
        return: tuple like (25, 13, 48.343 ,'N')
        """
        if value < 0:
            loc_value = loc[0]
        elif value > 0:
            loc_value = loc[1]
        else:
            loc_value = ""

        abs_value = abs(value)
        deg =  int(abs_value)
        t1 = (abs_value-deg)*60
        min = int(t1)
        sec = round((t1 - min)* 60, 5)
        
        return (deg, min, sec, loc_value)
        
    def get_latest_coor(self):
        if(self.coor_latest_message == 0):
            raise TopicException("No info from geo topic")
        return self.coor_latest_message
   
    def get_latest_coor_deg(self):
        coor       = self.get_latest_coor()
        result_deg = [self.to_deg(coor[0], ["S", "N"]),
                      self.to_deg(coor[1], ["W", "E"]),
                      coor[2]]
        #print(result_deg)
        return result_deg
        
    def get_latest_image(self):
        if self.is_img_sub:
            if self.image_latest_message == 0:
                raise TopicException("No info from image topic")
            else:
                cv2_img = self.bridge.imgmsg_to_cv2(self.image_latest_message, "bgr8")
                return cv2_img
        else:
            raise TopicException("Not image subscriber")
            
    
class TopicException(Exception):
    def __init__(self, message):
        self.message = message
        print(message)