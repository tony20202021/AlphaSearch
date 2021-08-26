from Detectors import alpha_detector_squares_base

import cv2

import numpy as np

class OpenCV_text_computeNMChannels(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{5768DF10-BE84-49D9-A0DA-E326B7F9467D}'
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

        gray3 = np.stack((gray, gray, gray), axis=-1)
        channels = cv2.text.computeNMChannels(gray3)

        rects = []

        cn = len(channels) - 1
        for c in range(0, cn):
            channels.append((255 - channels[c]))

        for channel in channels:
            erc1 = cv2.text.loadClassifierNM1('trained_classifierNM1.xml')
            er1 = cv2.text.createERFilterNM1(erc1, 16, 0.00015, 0.13, 0.2, True, 0.1)

            erc2 = cv2.text.loadClassifierNM2('trained_classifierNM2.xml')
            er2 = cv2.text.createERFilterNM2(erc2, 0.5)

            regions = cv2.text.detectRegions(channel, er1, er2)

            # rects = cv2.text.erGrouping(gray3,channel,[r.tolist() for r in regions])
            # rects = cv2.text.erGrouping(gray3,channel,[x.tolist() for x in regions], cv2.text.ERGROUPING_ORIENTATION_ANY,'trained_classifier_erGrouping.xml',0.5)

            if (regions is not None):
                rects.extend([cv2.boundingRect(p.reshape(-1, 1, 2)) for p in regions])

        if self.__SHOW and (len(rects) > 0):
            self.show_detected(gray, height, width, rects)

        points = []

        return self.process_rects(frame_index, rects, height, width, Items, value_last)


    def show_detected(self, image, height, width, rects):
        gray = image
        gray3 = np.stack((gray, gray, gray), axis=-1)

        for r in range(0,np.shape(rects)[0]):
            rect = rects[r]
            cv2.rectangle(gray3, (rect[0],rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (0, 0, 0), 2)
            cv2.rectangle(gray3, (rect[0],rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (255, 255, 255), 1)

        # cv2.destroyAllWindows()
        cv2.imshow("show", gray3)
        cv2.waitKey(1)



# import sys
# import os
#
# import cv2 as cv
# import numpy as np
#
# print('\ntextdetection.py')
# print('       A demo script of the Extremal Region Filter algorithm described in:')
# print('       Neumann L., Matas J.: Real-Time Scene Text Localization and Recognition, CVPR 2012\n')
#
#
# if (len(sys.argv) < 2):
#   print(' (ERROR) You must call this script with an argument (path_to_image_to_be_processed)\n')
#   quit()
#
# pathname = os.path.dirname(sys.argv[0])
#
#
# img      = cv.imread(str(sys.argv[1]))
# # for visualization
# vis      = img.copy()
#
#
# # Extract channels to be processed individually
# channels = cv.text.computeNMChannels(img)
# # Append negative channels to detect ER- (bright regions over dark background)
# cn = len(channels)-1
# for c in range(0,cn):
#   channels.append((255-channels[c]))
#
# # Apply the default cascade classifier to each independent channel (could be done in parallel)
# print("Extracting Class Specific Extremal Regions from "+str(len(channels))+" channels ...")
# print("    (...) this may take a while (...)")
# for channel in channels:
#
#   erc1 = cv.text.loadClassifierNM1(pathname+'/trained_classifierNM1.xml')
#   er1 = cv.text.createERFilterNM1(erc1,16,0.00015,0.13,0.2,True,0.1)
#
#   erc2 = cv.text.loadClassifierNM2(pathname+'/trained_classifierNM2.xml')
#   er2 = cv.text.createERFilterNM2(erc2,0.5)
#
#   regions = cv.text.detectRegions(channel,er1,er2)
#
#   rects = cv.text.erGrouping(img,channel,[r.tolist() for r in regions])
#   #rects = cv.text.erGrouping(img,channel,[x.tolist() for x in regions], cv.text.ERGROUPING_ORIENTATION_ANY,'../../GSoC2014/opencv_contrib/modules/text/samples/trained_classifier_erGrouping.xml',0.5)
#
#   #Visualization
#   for r in range(0,np.shape(rects)[0]):
#     rect = rects[r]
#     cv.rectangle(vis, (rect[0],rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (0, 0, 0), 2)
#     cv.rectangle(vis, (rect[0],rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (255, 255, 255), 1)
#
#
# #Visualization
# cv.imshow("Text detection result", vis)
# cv.waitKey(0)
