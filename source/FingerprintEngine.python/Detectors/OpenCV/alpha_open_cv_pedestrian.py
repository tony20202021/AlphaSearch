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

class OpenCV_Pedestrian(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{720C3744-1D72-4F0F-A817-A8DF9C2ABC9D}'
    f_version = 3

    __PARAMS = {
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,
    }

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

    def process_frame(self, frame_index, image, height, width, Item_FingerPrintOne, value_last):
        value = 0
        change = 0

        gray = image[:height * width].reshape([height, width])

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        (rects, weights) = hog.detectMultiScale(gray, winStride=(4, 4), padding=(8, 8), scale=1.05)

        return self.process_rects(frame_index, rects, height, width, Item_FingerPrintOne, value_last)

    def show_detected(self, image, height, width):
        gray = image
        gray3 = np.stack((gray, gray, gray), axis=-1)
        # viewImage(gray3, 'original')

        # orig = gray3.copy()
        # image = gray3.copy()

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # detect people in the image
        (rects, weights) = hog.detectMultiScale(gray, winStride=(4, 4), padding=(8, 8), scale=1.05)

        # draw the original bounding boxes
        for (x, y, w, h) in rects:
            cv2.rectangle(gray3, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # apply non-maxima suppression to the bounding boxes using a
        # fairly large overlap threshold to try to maintain overlapping
        # boxes that are still people
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        # draw the final bounding boxes
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(gray3, (xA, yA), (xB, yB), (0, 255, 0), 2)

        cv2.imshow("all", gray3)
        cv2.waitKey(0)

        # cv2.imshow("Before NMS", orig)
        # cv2.imshow("After NMS", image)
        # cv2.waitKey(0)

        # gray4 = np.copy(gray3)
        # cv2.drawContours(gray4, contours, -1, (0, 0, 255), 3)
        # viewImage(gray4, 'all')
