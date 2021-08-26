from Detectors import alpha_detector_squares_base

import cv2
from imutils.object_detection import non_max_suppression

import numpy as np

class OpenCV_SIFT(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{2B511826-BC34-41F9-9F62-0C0E610C7306}'
    f_version = 1
    __PARAMS = {
        'threshold_limit': 20,
        'squares_count': 10,
        'roll_frames_count': 5,
    }
    __SHOW = None

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = False

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        gray = image[:height * width].reshape([height, width])

        sift = cv2.SIFT_create()
        key_points = sift.detect(gray, None)

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

        img = cv2.drawKeypoints(gray, key_points, gray3)

        # cv2.destroyAllWindows()
        cv2.imshow("show", img)
        cv2.waitKey(1)



# import numpy as np
# import cv2 as cv
# img = cv.imread('home.jpg')
# gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# sift = cv.SIFT_create()
# kp = sift.detect(gray,None)
# img=cv.drawKeypoints(gray,kp,img)
# cv.imwrite('sift_keypoints.jpg',img)