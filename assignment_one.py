#!/usr/bin/env python
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
#call rosbag play image.bag --loop and run this node in new file
def callback(msg):
    bridge = CvBridge()
    orig = bridge.imgmsg_to_cv2(msg, "bgr8")
    orig= cv2.GaussianBlur(orig,(5,5),0)
    imgrey=cv2.cvtColor(orig,cv2.COLOR_BGR2GRAY)
    _,thrash=cv2.threshold(imgrey,60,255,cv2.THRESH_BINARY)
    #cv2.imshow('thrash',thrash)
    #cv2.waitKey(2000)
    img,contour, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for c in contour:
        approx=cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
        cv2.drawContours(orig,[approx],0,(0,0,0),2)
        cv2.imshow('image',orig)
        cv2.waitKey(2000)
        x, y, w, h = cv2.boundingRect(c)
        rospy.loginfo("COORDINATES ARE -: %f , %f",(x+w/2),(y-h/2))

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/magnus/camera/image_raw', Image, callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
