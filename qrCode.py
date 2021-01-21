#!/usr/bin/env python

import rospy
import cv2
import sys
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from pyzbar.pyzbar import decode

class Camera1:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/eyrc/vb/camera_1/image_raw", Image,self.callback)
    #self.pack_color = None
 
  def get_qr_data(self, img):
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #for x in range(0, len(hsv)):
        #for y in range(0, len(hsv[0])):
            #hsv[x,y][2] += value
    #img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    output_codes = decode(img)
    print(output_codes)
    #contrast_img = cv2.addWeighted(img, 2.5, 1, 1)
    #print(type(output_codes))
    #print(len(output_codes))
    #mylist=[]
    for code in output_codes:
        #x, y , w, h = code.rect
        #barcode_info = code.data.decode('utf-8')
        #cv2.rectangle(img, (x, y),(x+w, y+h), (0, 255, 0), 2)
	#font = cv2.FONT_HERSHEY_DUPLEX
        #cv2.putText(img, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        #with open("barcode_result.txt", mode ='w') as file:
            #file.write("Recognized Barcode:" + barcode_info)
        #a=list(code.split(" "))
        print(code)
        
   	print('data: ', code.data)
    	print('type: ', code.type)
    	#print('rect: ', code.rect)
    	#print('polygon:', code.polygon)
        #self.pack_color = code.data
        #return self.pack_color

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      rospy.logerr(e)

    (rows,cols,channels) = cv_image.shape
    
    img = cv_image
    image = cv2.addWeighted(img, 5, np.zeros(img.shape, img.dtype), 0, 0)
    lst = {}
    while True:
        for qr_result in decode(image):
            print(qr_result)
            #lst.append(qr_result)
            mydata = qr_result.data.decode('utf-8')
            lst.update({'package00':mydata,'package01':mydata,'package02':mydata})
            print(lst)
            #print(type(mydata))
            pts = np.array([qr_result.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(image,[pts],True,(255,0,255),5)
            pts2 = qr_result.rect
            cv2.putText(image,mydata,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
            
#dicta.append(qr_result)   = {
#{'package00': [Point(x=318, y=797), Point(x=318, y=886), Point(x=407, y=886), Point(x=407, y=797)],'package01': [Point(x=129, y=643), Point(x=129, y=733), Point(x=218, y=733), Point(x=218, y=644)]
            
    # Resize a 720x1280 image to 360x640 to fit it on the screen
            resized_image = cv2.resize(image, (720/2, 1280/2)) 

            cv2.imshow("/eyrc/vb/camera_1/image_raw", resized_image)
            break
    
            rospy.loginfo(self.get_qr_data(image))
    
            cv2.waitKey(1)
          
        #print(lst)

def main(args):
  
  rospy.init_node('node_eg3_qr_decode', anonymous=True)

  ic = Camera1()
  
  try:
    rospy.spin()
  except KeyboardInterrupt:
    rospy.loginfo("Shutting down")
  
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
