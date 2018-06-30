import cv2 as cv
import time
import numpy as np
import math
import pyautogui as robot
import webbrowser
from Controller import  Controller



#cass declaration for the project only only class for the hand gesture recognization.
##ROI means region of intrest
class HandGesture:
    def __init__(self):
        self.frame = None
        self.video = cv.VideoCapture(0)
        self.bgfg = cv.BackgroundSubtractorMOG2()
        self.image = None
        self.crop_image = None
        self.gray = None
        self.blurred = None
        self.background = None
        self.thresh = None
        self.contour = None
        self.hull = None
        self.defects = None
        self.mask = None
        self.drawing = None


    def captureVideo(self):
        #this function is used to start the webcam
        flag,self.frame = self.video.read()
        if flag == False:
            print('the webcam is not working properly')
            exit()

    def drawWindow(self,x1,x2,y1,y2):
        #this function is used to take ROI and get the ROI
        cv.rectangle(self.frame, (x1-1,x2-1), (y1+1, y2+1), (255, 0, 0), 0)
        cv.imshow('frame', self.frame)
        self.crop_image = self.frame[x1:y1,x2:y2]
    def createMask(self):
        #this function is used to remove the background and apply threshold means the turning the
        ##image to binary that means we will see the image i black and white
        self.mask = self.bgfg.apply(self.crop_image)
        self.blurred = cv.GaussianBlur(self.mask,(35,35),0)
        _,self.thresh = cv.threshold(self.blurred,127,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
        cv.imshow('threshed',self.thresh)
    def findContour(self):
        #find countours,ie the closed shapes and after we find all the shapes we select the biggest one
        #because that would be our hand
        self.contour,_ = cv.findContours(self.thresh.copy(),cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
        return len(self.contour)
    def drawContour(self):
        #drawing the shapes on the screen
        self.contour = max(self.contour,key=lambda x:cv.contourArea(x))
        self.drawing = np.zeros(self.crop_image.shape,np.uint8)
        x,y,w,h = cv.boundingRect(self.contour)
        cv.rectangle(self.crop_image,(x,y),(x+w,y+h),(255,0,0),0)
        cv.drawContours(self.drawing,[self.contour],-1,(0,255,0),0)

    def findHull(self):
        #finding convex hull that means finding the outermost pointer in our shape
        self.hull = cv.convexHull(self.contour)
        cv.drawContours(self.drawing,[self.hull],0,(0,0,255),0)
        cv.imshow('drawing',self.drawing)

    def findDefects(self):

        self.hull = cv.convexHull(self.contour,returnPoints=False)
        self.defects = cv.convexityDefects(self.contour,self.hull)
        return self.defects
    def countAngle(self):
        # finding the number of angles present in our project
        count_defects = 0
        for i in range(self.defects.shape[0]):
            s,e,f,d = self.defects[i,0]

            start = tuple(self.contour[s][0])
            end = tuple(self.contour[e][0])
            far = tuple(self.contour[f][0])

            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)


            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

            if angle <=90:
                count_defects +=1
                cv.circle(self.drawing,far,1,(0,0,255),-1)

        return count_defects




#main function
def main():
     hand = HandGesture()
     connection = Controller()
     flag = 0
     while True:
        hand.captureVideo()
        hand.drawWindow(100,100,350,350)
        hand.createMask()
        length = hand.findContour()
        if length ==0:
            continue
        hand.drawContour()
        hand.findHull()
        defects = hand.findDefects()
        if defects==None:
            continue
        fingers = hand.countAngle()

        if fingers ==1:
            print('2 fingers')
           # connection.forward()
            if flag==1:
                robot.press('a')

        elif fingers ==2:
            print('3 fingers')
            # connection.backward()
            if flag==1:
                robot.press('d')
        elif fingers ==3:
            print ('4 fingers')
           # connection.turnLeft()
            if flag==1:
                robot.press('space')
        elif fingers ==4:
            print('5 fingers')
           # connection.turnRight()
            if flag==0:
                webbrowser.open('file:///C:/Users/Win%2010/Desktop/game/game.html')
                flag =1
        else:
            pass
            connection.stop()



        if cv.waitKey(2) & 0xFF == ord('w'):
            flag = 1
        if cv.waitKey(1) & 0xFF == ord('q'):
            connection.stop()
            break





main()


