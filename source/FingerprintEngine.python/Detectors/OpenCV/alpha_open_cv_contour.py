from Detectors import alpha_detector_squares_base
import alpha_show_graphics

import cv2

import numpy as np


def viewImage(image, title='title'):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def findGreatesContour(contours):
    largest_area = 0
    largest_contour_index = -1
    i = 0
    total_contours = len(contours)
    while (i < total_contours):
        area = cv2.contourArea(contours[i])
        if (area > largest_area):
            largest_area = area
            largest_contour_index = i
        i += 1

    return largest_area, largest_contour_index

class OpenCV_Contour(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{C970D0D2-5925-4118-BE0A-BDA216EE1D3C}'
    f_version = 2

    __PARAMS = {
        'squares_count': 10,
        'roll_frames_count': 1,
        'area_limit_min': 0.01,
        'area_limit_max': 0.50,
        'threshold_limit': 127,
    }

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

    def process_frame(self, frame_index, image, height, width, Item_FingerPrintOne, value_last):
        value = 0
        change = 0

        gray = image[:height * width].reshape([height, width])

        area_total = height * width

        ret, threshold = cv2.threshold(gray, self.f_params['threshold_limit'], 255, 0)
        contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        detected = [c for c in contours if (cv2.contourArea(c) > self.f_params['area_limit_min'] * area_total) and (
                cv2.contourArea(c) < self.f_params['area_limit_max'] * area_total)]

        show = False #(frame_index == 200)
        if show:
            self.show_detected(image, height, width, contours, detected)

        return self.process_rects(frame_index, detected, height, width, Item_FingerPrintOne, value_last)


    def show_detected(self, image, height, width, contours, detected):

        gray = image[:height * width].reshape([height, width])
        gray3 = np.stack((gray, gray, gray), axis=-1)
        # viewImage(gray3, 'original')

        # viewImage(threshold, 'threshold ' + str(__THRESHOLD_LIMIT))

        gray4 = np.copy(gray3)
        cv2.drawContours(gray4, contours, -1, (0, 0, 255), 3)
        viewImage(gray4, 'all')

        area_total = height * width

        areas = [cv2.contourArea(c) for c in contours]
        areas_filtered = [cv2.contourArea(c) for c in contours if
                          (cv2.contourArea(c) > self.f_params['area_limit_min'] * area_total) and (
                                      cv2.contourArea(c) < self.f_params['area_limit_max'] * area_total)]

        largest_area, largest_contour_index = findGreatesContour(contours)
        # gray4 = np.copy(gray3)
        # contour = contours[largest_contour_index]
        # area = cv2.contourArea(contour)
        # cv2.drawContours(gray4, contour, -1, (0, 0, 255), 3)
        # x, y, w, h = cv2.boundingRect(contour)
        # cv2.rectangle(gray4, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # viewImage(gray4, 'largest_area')

        gray4 = np.copy(gray3)
        cv2.drawContours(gray4, detected, -1, (0, 0, 255), 3)
        viewImage(gray4, 'detected')

        for contour in detected:
            gray4 = np.copy(gray3)
            area = cv2.contourArea(contour)
            cv2.drawContours(gray4, contour, -1, (0, 0, 255), 3)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(gray4, (x, y), (x + w, y + h), (0, 255, 0), 2)
            viewImage(gray4, 'detected: area={:.2f}'.format(area / area_total))

        # areas = [cv2.contourArea(c) for c in contours]