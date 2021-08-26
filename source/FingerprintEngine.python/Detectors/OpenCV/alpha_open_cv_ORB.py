from Detectors import alpha_detector_squares_base

import cv2

import numpy as np

class OpenCV_ORB(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{9A9DEE5E-6F98-4D1D-9C75-BEA3C4AA43CA}'
    f_version = 1
    __PARAMS = {
        'threshold_limit_total': 0.8,
        'threshold_limit_squares_sum_exact': 0.7,
        'threshold_limit_squares_sum': 0.5,
        'threshold_limit_squares_max': 999999,
        'squares_count': 10,
        'roll_frames_count': 2,
    }
    f_frames_all = None

    __SHOW = None


    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = False

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        gray = image[:height * width].reshape([height, width])

        orb = cv2.ORB_create()
        # find the keypoints with ORB
        key_points = orb.detect(gray, None)
        # compute the descriptors with ORB
        # key_points, des = orb.compute(gray, key_points)

        points = [] if (key_points is None) else [{'x': kp.pt[0], 'y': kp.pt[1]} for kp in key_points]

        result = self.process_points(frame_index, points, height, width, Items, value_last, is_binary=True)

        if self.__SHOW:
            value_last_average = None if value_last is None else value_last['average']
            squares_average = result['average']

            need_show = False
            if frame_index != result['frame_index_for_save']:
                if self.f_frames_all is None:
                    self.f_frames_all = []

                self.f_frames_all.append({'image': gray, 'key_points': key_points, 'frame_index': frame_index})

                if result['frame_index_for_save'] is None:
                    need_show = False
                else:
                    need_show = True

                    if len(self.f_frames_all) > (frame_index - result['frame_index_for_save']):
                        self.f_frames_all = self.f_frames_all[-1 - (frame_index - result['frame_index_for_save']):]

                    assert(self.f_frames_all[0]['frame_index'] == result['frame_index_for_save'])

                    key_points_for_show = self.f_frames_all[0]['key_points']
                    image_for_show = self.f_frames_all[0]['image']
            else:
                need_show = True

                key_points_for_show = key_points
                image_for_show = gray

            if need_show:
                self.show_detected(key_points_for_show,
                                   image_for_show,
                                   frame_index, result['frame_index_for_save'],
                                   height, width,
                                   value_last_average, squares_average, result['squares_diff_exact'], result['squares_diff_shifted'],
                                   result['change_total'], result['change_squares_sum_exact'], result['change_squares_sum'], result['change_squares_max'],
                                   result['is_change_total'], result['is_change_squares_sum_exact'], result['is_change_squares_sum'], result['is_change_squares_max'])

        return result


    def show_detected(self, key_points,
                      image,
                      frame_index, frame_index_for_save,
                      height, width,
                      value_last_average, squares_average, squares_diff_exact, squares_diff_shifted,
                      change_total, change_squares_sum_exact, change_squares_sum, change_squares_max,
                      is_change_total, is_change_squares_sum_exact, is_change_squares_sum, is_change_squares_max):
        gray = image
        gray3 = np.stack((gray, gray, gray), axis=-1)

        gray3 = cv2.drawKeypoints(gray3, key_points, None, color=(0, 255, 0), flags=0)

        super().show_detected(
                      gray3,
                      frame_index, frame_index_for_save,
                      height, width,
                      value_last_average, squares_average, squares_diff_exact, squares_diff_shifted,
                      change_total, change_squares_sum_exact, change_squares_sum, change_squares_max,
                      is_change_total, is_change_squares_sum_exact, is_change_squares_sum, is_change_squares_max)



# import numpy as np
# import cv2 as cv
# from matplotlib import pyplot as plt
# img = cv.imread('simple.jpg',0)
# # Initiate ORB detector
# orb = cv.ORB_create()
# # find the keypoints with ORB
# kp = orb.detect(img,None)
# # compute the descriptors with ORB
# kp, des = orb.compute(img, kp)
# # draw only keypoints location,not size and orientation
# img2 = cv.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)
# plt.imshow(img2), plt.show()