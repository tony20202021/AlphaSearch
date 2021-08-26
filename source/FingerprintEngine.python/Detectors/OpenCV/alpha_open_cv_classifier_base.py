from Detectors import alpha_detector_squares_base
import alpha_show_graphics

import cv2

import numpy as np


class OpenCV_Base(alpha_detector_squares_base.Detector_Squares_Base):
    f_version = 3

    def process_frame(self, frame_index, image, height, width, Item_FingerPrintOne, value_last):
        value = 0
        change = 0

        gray = image[:height * width].reshape([height, width])

        cascade = cv2.CascadeClassifier(self.f_params['config_file'])
        rects = cascade.detectMultiScale(gray,
                                            scaleFactor=self.f_params['scaleFactor'],
                                            minNeighbors=self.f_params['minNeighbors'],
                                            minSize=self.f_params['minSize']
                                            )

        result = self.process_rects(frame_index, rects, height, width, Item_FingerPrintOne, value_last)

        value_last_average = None if value_last is None else value_last['average']
        squares_average = result['average']

        self.show_detected(image,
                      frame_index, result['frame_index_for_save'],
                      height, width,
                      value_last_average, squares_average, result['squares_diff'],
                      result['change_total'], result['change_squares_sum'], result['change_squares_max'],
                      result['is_change_total'], result['is_change_squares_sum'], result['is_change_squares_max'])

        return result


