from Detectors import alpha_detector_squares_base

import cv2
from imutils.object_detection import non_max_suppression

import numpy as np

class OpenCV_Corners_Base(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = None
    f_version = None
    __PARAMS = None
    __SHOW = None

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = None

    def detect(self, gray):
        return None

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        gray = image[:height * width].reshape([height, width])

        dst = self.detect(gray)
        dst = cv2.dilate(dst, None)

        if self.__SHOW and (dst is not None):
            self.show_detected(gray, height, width, dst)

        return self.process_pixels(frame_index, dst, self.f_params['threshold'] * dst.max(), height, width, Items, value_last)


    def show_detected(self, image, height, width, dst):
        gray = image
        gray3 = np.stack((gray, gray, gray), axis=-1)

        gray3[dst > self.f_params['threshold'] * dst.max()] = [0, 0, 255]

        cv2.destroyAllWindows()
        cv2.imshow("show", gray3)
        cv2.waitKey(500)


class OpenCV_Corners_Harris(OpenCV_Corners_Base):
    f_id = '{A0FA1A87-188C-442B-812A-AAA123F8CB2A}'
    f_version = 2

    __PARAMS = {
        'threshold_limit': 200,
        'squares_count': 10,
        'roll_frames_count': 5,
        'blockSize': 2,
        'ksize': 3,
        'k': 0.04,
        'threshold': 0.04,
    }

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = False

    def detect(self, gray):
        return cv2.cornerHarris(gray, blockSize=self.f_params['blockSize'], ksize=self.f_params['ksize'], k=self.f_params['k'])


class OpenCV_Corners_MinEigenVal(OpenCV_Corners_Base):
    f_id = '{620D5D10-39FC-4995-B979-4541377816B3}'
    f_version = 2

    __PARAMS = {
        'threshold_limit': 400,
        'squares_count': 10,
        'roll_frames_count': 5,
        'blockSize': 2,
        'ksize': 3,
        'k': 0.04,
        'threshold': 0.07,
    }

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = False

    def detect(self, gray):
        return cv2.cornerMinEigenVal(gray, blockSize=self.f_params['blockSize'], ksize=self.f_params['ksize'])





# import numpy as np
# import cv2 as cv
# filename = 'chessboard.png'
# img = cv.imread(filename)
# gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# gray = np.float32(gray)
# dst = cv.cornerHarris(gray,2,3,0.04)
# #result is dilated for marking the corners, not important
# dst = cv.dilate(dst,None)
# # Threshold for an optimal value, it may vary depending on the image.
# img[dst>0.01*dst.max()]=[0,0,255]
# cv.imshow('dst',img)
# if cv.waitKey(0) & 0xff == 27:
#     cv.destroyAllWindows()
