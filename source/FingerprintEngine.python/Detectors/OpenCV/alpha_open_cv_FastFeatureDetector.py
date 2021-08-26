from Detectors import alpha_detector_squares_base

import cv2
from imutils.object_detection import non_max_suppression
import numpy as np

class OpenCV_FastFeatureDetector(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{74C91588-F25B-468D-A6E7-0C5F69BF3729}'
    f_version = 1
    __PARAMS = {
        'threshold_limit': 300,
        'squares_count': 10,
        'roll_frames_count': 5,

    }
    __SHOW = None

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = False

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        gray = image[:height * width].reshape([height, width])

        fast = cv2.FastFeatureDetector_create()
        # fast.setNonmaxSuppression(0) #fast.getNonmaxSuppression()
        key_points = fast.detect(gray, None)

        if (key_points is None):
            points = []
        else:
            points = [{'x': kp.pt[0], 'y': kp.pt[1]} for kp in key_points]

        if self.__SHOW and (key_points is not None):
            self.show_detected(gray, height, width, key_points)

        return self.process_points(frame_index, points, height, width, Items, value_last)


    def show_detected(self, image, height, width, key_points):
        gray = image
        gray3 = np.stack((gray, gray, gray), axis=-1)

        img = cv2.drawKeypoints(gray3, key_points, None, (255, 0, 0), 4)

        # cv2.destroyAllWindows()
        cv2.imshow("show", img)
        cv2.waitKey(1)




# import numpy as np
# import cv2 as cv
# from matplotlib import pyplot as plt
# img = cv.imread('simple.jpg',0)
# # Initiate FAST object with default values
# fast = cv.FastFeatureDetector_create()
# # find and draw the keypoints
# kp = fast.detect(img,None)
# img2 = cv.drawKeypoints(img, kp, None, color=(255,0,0))
# # Print all default params
# print( "Threshold: {}".format(fast.getThreshold()) )
# print( "nonmaxSuppression:{}".format(fast.getNonmaxSuppression()) )
# print( "neighborhood: {}".format(fast.getType()) )
# print( "Total Keypoints with nonmaxSuppression: {}".format(len(kp)) )
# cv.imwrite('fast_true.png',img2)
# # Disable nonmaxSuppression
# fast.setNonmaxSuppression(0)
# kp = fast.detect(img,None)
# print( "Total Keypoints without nonmaxSuppression: {}".format(len(kp)) )
# img3 = cv.drawKeypoints(img, kp, None, color=(255,0,0))
# cv.imwrite('fast_false.png',img3)