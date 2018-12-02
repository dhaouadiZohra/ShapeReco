#Dhaouadi Zohra Shape Recognition, simple version
#zohra.dhaouadi@esprit.tn
#Verion 3.7.1 latest version
#The Python Standard Library
#OpenCV library 3.4.1
#Biblio declaration
#Mathematical functions package
import math
#Numpy is a optimized library for fast array calculations
#Numpy provides a large set of numeric datatypes
#used to construct arrays.
#np is to rename the numerical python package 
import numpy as np
#import OpenCV module for binding and array conversion
import cv2

#OpenCV Contours python
contours = {}
#For testing approximate equality numbers
approx = []
#static dec number
scale = 2
#VideoCapture object declaration
#find the webcam
caption = cv2.VideoCapture("test.mp4")
#EXIT
print("press q to kill proc or change the line 108 : if cv2.waitKey(1) == 1048689 with if cv2.waitKey(0) == 1048689 run and click Enter to slower the record speed")

# Record
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#video output name,type, size
out = cv2.VideoWriter('zhra.avi',fourcc, 20.0, (640,480))

#Calcule angle
def angle(pt1,pt2,pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]
    return float((dx1*dx2 + dy1*dy2))/math.sqrt(float((dx1*dx1 + dy1*dy1))*(dx2*dx2 + dy2*dy2) + 1e-10)
#While recording do
while(caption.isOpened()):
 #Capture the frame
    ret, frame = caption.read()
    if ret==True:
          #Gray color
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #background caption black and white
        canny = cv2.Canny(frame,80,240,3)
#Contours detection, counter declaration
#Approximate the contour scale with a proportional number to the perimeter large    
        canny2, contours, hierarchy = cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in range(0,len(contours)):
   
            approx = cv2.approxPolyDP(contours[i],cv2.arcLength(contours[i],True)*0.02,True)

        #Ignore small objects
            if(abs(cv2.contourArea(contours[i]))<100 or not(cv2.isContourConvex(approx))):
                continue

            #Triangle with 3 sides shades
            if(len(approx) == 3):
                x,y,w,h = cv2.boundingRect(contours[i])
                cv2.putText(frame,'Triangle',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
                #More than 4 sides and less than 6
            elif(len(approx)>=4 and len(approx)<=6):
            #Polygonal curve
                vtc = len(approx)
         #Apply cos function on all cruves sides
                cos = []
                for j in range(2,vtc+1):
                    cos.append(angle(approx[j%vtc],approx[j-2],approx[j-1]))
             #sort in an ascending order all the results to be compared later
                cos.sort()
              
                mincos = cos[0]
                maxcos = cos[-1]

    #From the obtained numbers above ,  determine the shape of the objects
                x,y,w,h = cv2.boundingRect(contours[i])
                if(vtc==4):#Rectancle, Carré
                    cv2.putText(frame,'Quadrilateral',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
                elif(vtc==5):#Pentagon
                    cv2.putText(frame,'Pentagon',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
                elif(vtc==6):#Hexagon
                    cv2.putText(frame,'hexagon',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
            else:
                #circle, Area and surface calculation
                area = cv2.contourArea(contours[i])
                x,y,w,h = cv2.boundingRect(contours[i])
                radius = w/2
                if(abs(1 - (float(w)/h))<=2 and abs(1-(area/(math.pi*radius*radius)))<=0.2):
                    cv2.putText(frame,'Circle',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)

        #Results view
        out.write(frame)
        cv2.imshow('Scene',frame)
        cv2.imshow('Canva',canny)
        if cv2.waitKey(1) == 1048689:#Kill proc of displaying the window on openCV with any key pressed
            break
#End of loop conditio , otherwise we'll be in an infinite loop
#As a result the camera will no longer display only a green screen will show up
caption.release()#CloseAll
cv2.destroyAllWindows()#CleanAll
