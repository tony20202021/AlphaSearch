from Detectors import alpha_detector_squares_base

import cv2

import numpy as np

class OpenCV_text(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{3C8674DB-7C5C-4272-A05F-3AEC9A2929D8}'
    f_version = 1
    __PARAMS = {
        'threshold_limit': 5,
        'squares_count': 10,
        'roll_frames_count': 5,
    }
    __SHOW = None

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = False

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        gray = image[:height * width].reshape([height, width])

        erc1 = cv2.text.loadClassifierNM1('trained_classifierNM1.xml')
        er1 = cv2.text.createERFilterNM1(erc1)

        erc2 = cv2.text.loadClassifierNM2('trained_classifierNM2.xml')
        er2 = cv2.text.createERFilterNM2(erc2)

        regions = cv2.text.detectRegions(gray, er1, er2)

        if (regions is not None):
            rects = [cv2.boundingRect(p.reshape(-1, 1, 2)) for p in regions]
        else:
            rects = []

        if self.__SHOW and (regions is not None):
            self.show_detected(gray, height, width, rects)

        return self.process_rects(frame_index, rects, height, width, Items, value_last)


    def show_detected(self, image, height, width, rects):
        gray = image
        gray3 = np.stack((gray, gray, gray), axis=-1)

        for rect in rects:
          cv2.rectangle(gray3, rect[0:2], (rect[0]+rect[2],rect[1]+rect[3]), (0, 0, 0), 2)
        for rect in rects:
          cv2.rectangle(gray3, rect[0:2], (rect[0]+rect[2],rect[1]+rect[3]), (255, 255, 255), 1)

        # cv2.destroyAllWindows()
        cv2.imshow("show", gray3)
        cv2.waitKey(1)



# import sys
# import os
#
# import cv2 as cv
# import numpy as np
#
# print('\ndetect_er_chars.py')
# print('       A simple demo script using the Extremal Region Filter algorithm described in:')
# print('       Neumann L., Matas J.: Real-Time Scene Text Localization and Recognition, CVPR 2012\n')
#
#
# if (len(sys.argv) < 2):
#   print(' (ERROR) You must call this script with an argument (path_to_image_to_be_processed)\n')
#   quit()
#
# pathname = os.path.dirname(sys.argv[0])
#
# img  = cv.imread(str(sys.argv[1]))
# gray = cv.imread(str(sys.argv[1]),0)
#
# erc1 = cv.text.loadClassifierNM1(pathname+'/trained_classifierNM1.xml')
# er1 = cv.text.createERFilterNM1(erc1)
#
# erc2 = cv.text.loadClassifierNM2(pathname+'/trained_classifierNM2.xml')
# er2 = cv.text.createERFilterNM2(erc2)
#
# regions = cv.text.detectRegions(gray,er1,er2)
#
# #Visualization
# rects = [cv.boundingRect(p.reshape(-1, 1, 2)) for p in regions]
# for rect in rects:
#   cv.rectangle(img, rect[0:2], (rect[0]+rect[2],rect[1]+rect[3]), (0, 0, 0), 2)
# for rect in rects:
#   cv.rectangle(img, rect[0:2], (rect[0]+rect[2],rect[1]+rect[3]), (255, 255, 255), 1)
# cv.imshow("Text detection result", img)
# cv.waitKey(0)