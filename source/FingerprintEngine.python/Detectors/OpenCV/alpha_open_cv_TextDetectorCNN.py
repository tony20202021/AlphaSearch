from Detectors import alpha_detector_squares_base

import cv2

import numpy as np

class OpenCV_TextDetectorCNN(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{DD470B85-8472-4D6A-A2CF-5B8C53F0A405D}'
    f_version = 1
    __PARAMS = {
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,
        'thres': 0.6,
    }
    __SHOW = None

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = True

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        gray = image[:height * width].reshape([height, width])
        gray3 = np.stack((gray, gray, gray), axis=-1)

        textSpotter = cv2.text.TextDetectorCNN_create("textbox.prototxt", "TextBoxes_icdar13.caffemodel")
        det, outProbs = textSpotter.detect(gray3)

        rects = []
        if (det is not None):
            for r in range(np.shape(det)[0]):
                if outProbs[r] > self.f_params['thres']:
                    rects.append(det[r])

        if self.__SHOW and (len(rects) > 0):
            self.show_detected(gray, height, width, rects)

        return self.process_rects(frame_index, rects, height, width, Items, value_last)


    def show_detected(self, image, height, width, rects):
        gray = image
        gray3 = np.stack((gray, gray, gray), axis=-1)

        for rect in rects:
            cv2.rectangle(gray3, (rect[0],rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 2)

        # cv2.destroyAllWindows()
        cv2.imshow("show", gray3)
        cv2.waitKey(1)



# import sys
# import os
# import cv2 as cv
# import numpy as np
#
# def main():
#     print('\nDeeptextdetection.py')
#     print('       A demo script of text box alogorithm of the paper:')
#     print('       * Minghui Liao et al.: TextBoxes: A Fast Text Detector with a Single Deep Neural Network https://arxiv.org/abs/1611.06779\n')
#
#     if (len(sys.argv) < 2):
#         print(' (ERROR) You must call this script with an argument (path_to_image_to_be_processed)\n')
#         quit()
#
#     if not os.path.isfile('TextBoxes_icdar13.caffemodel') or not os.path.isfile('textbox.prototxt'):
#         print " Model files not found in current directory. Aborting"
#         print " See the documentation of text::TextDetectorCNN class to get download links."
#         quit()
#
#     img = cv.imread(str(sys.argv[1]))
#     textSpotter = cv.text.TextDetectorCNN_create("textbox.prototxt", "TextBoxes_icdar13.caffemodel")
#     rects, outProbs = textSpotter.detect(img);
#     vis = img.copy()
#     thres = 0.6
#
#     for r in range(np.shape(rects)[0]):
#         if outProbs[r] > thres:
#             rect = rects[r]
#             cv.rectangle(vis, (rect[0],rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 2)
#
#     cv.imshow("Text detection result", vis)
#     cv.waitKey()
#
# if __name__ == "__main__":
#     main()
