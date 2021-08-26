from Detectors import alpha_detector_squares_base

import cv2
from imutils.object_detection import non_max_suppression

import numpy as np

class OpenCV_goodFeaturesToTrack(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{CB3E2C17-D362-4722-81F6-1EB9E1992BAD}'
    f_version = 1
    __PARAMS = {
        'threshold_limit': 4,
        'squares_count': 10,
        'roll_frames_count': 1,
        'maxCorners': 100,
        'qualityLevel': 0.04,
        'minDistance': 0.01

    }
    __SHOW = None

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = False

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        gray = image[:height * width].reshape([height, width])

        corners = cv2.goodFeaturesToTrack(
            gray,
            maxCorners=self.f_params['maxCorners'],
            qualityLevel=self.f_params['qualityLevel'],
            minDistance=self.f_params['minDistance'] * min(height, width)
        )
        # corners = np.int0(corners)

        if (corners is None):
            points = []
        else:
            points = [{'x': c[0][0], 'y': c[0][1]} for c in corners]

        if self.__SHOW and (corners is not None):
            self.show_detected(gray, height, width, corners)

        return self.process_points(frame_index, points, height, width, Items, value_last)


    def show_detected(self, image, height, width, corners):
        gray = image
        gray3 = np.stack((gray, gray, gray), axis=-1)

        # corners = np.int0(corners)
        for i in corners:
            x, y = i.ravel()
            cv2.circle(gray3,(x,y),3,255,-1)

        cv2.destroyAllWindows()
        cv2.imshow("show", gray3)
        cv2.waitKey(100)




#
# import numpy as np
# import cv2 as cv
# from matplotlib import pyplot as plt
# img = cv.imread('blox.jpg')
# gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# corners = cv.goodFeaturesToTrack(gray,25,0.01,10)
# corners = np.int0(corners)
# for i in corners:
#     x,y = i.ravel()
#     cv.circle(img,(x,y),3,255,-1)
# plt.imshow(img),plt.show()