from Detectors import alpha_detector_squares_base

import cv2

import numpy as np

class OpenCV_SelectiveSearchSegmentation(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{5300A64A-6BBF-4342-A9D0-CD94A5E0684D}'
    f_version = 1
    __PARAMS = {
        'threshold_limit': 2,
        'squares_count': 10,
        'roll_frames_count': 5,
        'switch': 's',
    }
    __SHOW = None

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = True

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        gray = image[:height * width].reshape([height, width])

        gs = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
        gray3 = np.stack((gray, gray, gray), axis=-1)
        gs.setBaseImage(gray3)

        if (self.f_params['switch'] == 's'):
            gs.switchToSingleStrategy()
        elif (self.f_params['switch'] == 'f'):
            gs.switchToSelectiveSearchFast()
        elif (self.f_params['switch'] == 'q'):
            gs.switchToSelectiveSearchQuality()

        rects = gs.process()

        if self.__SHOW and (rects is not None):
            self.show_detected(gray, height, width, rects)

        return self.process_rects(frame_index, rects, height, width, Items, value_last)


    def show_detected(self, image, height, width, rects):
        gray = image
        gray3 = np.stack((gray, gray, gray), axis=-1)

        for i in range(len(rects)):
            x, y, w, h = rects[i]
            cv2.rectangle(gray3, (x, y), (x+w, y+h), (0, 255, 0), 1, cv2.LINE_AA)

        # cv2.destroyAllWindows()
        cv2.imshow("show", gray3)
        cv2.waitKey(1)





# import cv2 as cv
# import sys
#
# if __name__ == '__main__':
#     img = cv.imread(sys.argv[1])
#
#     cv.setUseOptimized(True)
#     cv.setNumThreads(8)
#
#     gs = cv.ximgproc.segmentation.createSelectiveSearchSegmentation()
#     gs.setBaseImage(img)
#
#     if (sys.argv[2][0] == 's'):
#         gs.switchToSingleStrategy()
#
#     elif (sys.argv[2][0] == 'f'):
#         gs.switchToSelectiveSearchFast()
#
#     elif (sys.argv[2][0] == 'q'):
#         gs.switchToSelectiveSearchQuality()
#     else:
#         print(__doc__)
#         sys.exit(1)
#
#     rects = gs.process()
#     nb_rects = 10
#
#     while True:
#         wimg = img.copy()
#
#         for i in range(len(rects)):
#             if (i < nb_rects):
#                 x, y, w, h = rects[i]
#                 cv.rectangle(wimg, (x, y), (x+w, y+h), (0, 255, 0), 1, cv.LINE_AA)
#
#         cv.imshow("Output", wimg);
#         c = cv.waitKey()
#
#         if (c == 100):
#             nb_rects += 10
#
#         elif (c == 97 and nb_rects > 10):
#             nb_rects -= 10
#
#         elif (c == 113):
#             break
#
#     cv.destroyAllWindows()


