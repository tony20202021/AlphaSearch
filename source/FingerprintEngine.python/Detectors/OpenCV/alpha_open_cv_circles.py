from Detectors import alpha_detector_squares_base

import cv2
from imutils.object_detection import non_max_suppression

import numpy as np

stop_frame = 250

def viewImage(image, title='title'):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

class OpenCV_Circles(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{84411297-F72A-4D1A-9704-A68CDC5B5723}'
    f_version = 1

    __PARAMS = {
        'threshold_limit': 3,
        'squares_count': 10,
        'roll_frames_count': 5,
        'method': cv2.HOUGH_GRADIENT,
        'dp': 1,
        'minDist': 0.1,
        'param1': 50,
        'param2': 500,
        'minRadius': 0,
        'maxRadius': 0,
    }

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = False

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        value = 0
        change = 0

        gray = image[:height * width].reshape([height, width])

        # GaussianBlur()        with 7x7 kernel and 1.5x1.5
        circles = cv2.HoughCircles(
            gray,
            method=self.f_params['method'],
            dp=self.f_params['dp'],
            minDist=self.f_params['minDist'] * min(height, width),
            param1=self.f_params['param1'],
            param2=self.f_params['param2'],
            minRadius=self.f_params['minRadius'],
            maxRadius=self.f_params['maxRadius'])

        # circles = np.uint16(np.around(circles))

        rects = []
        if circles is not None:
            for c in circles[0,:]:
                x1 = int(c[0] - c[2])
                y1 = int(c[1] - c[2])
                x2 = int(c[0] + c[2])
                y2 = int(c[1] + c[2])
                rects.append([max(0, min(x1, x2)), max(0, min(y1, y2)), min(width, abs(x2-x1)), min(height, abs((y2-y1)))])

            if self.__SHOW and (len(circles) > 0):
                self.show_detected(gray, height, width, circles)

        return self.process_rects(frame_index, rects, height, width, Items, value_last)

    def show_detected(self, image, height, width, circles):
        gray = image
        gray3 = np.stack((gray, gray, gray), axis=-1)

        for c in circles[0,:]:
            # draw the outer circle
            cv2.circle(gray3,(c[0],c[1]),int(c[2]),(0,255,0),2)
            # draw the center of the circle
            cv2.circle(gray3,(c[0],c[1]),2,(0,0,255),3)

        cv2.destroyAllWindows()
        cv2.imshow("show", gray3)
        cv2.waitKey(500)







# import numpy as np
# import cv2 as cv
# img = cv.imread('opencv-logo-white.png',0)
# img = cv.medianBlur(img,5)
# cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
# circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,
#                             param1=50,param2=30,minRadius=0,maxRadius=0)
# circles = np.uint16(np.around(circles))
# for i in circles[0,:]:
#     # draw the outer circle
#     cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#     # draw the center of the circle
#     cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
# cv.imshow('detected circles',cimg)
# cv.waitKey(0)
# cv.destroyAllWindows()