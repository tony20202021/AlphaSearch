from Detectors import alpha_detector_squares_base

import numpy as np

# detector = dlib.get_frontal_face_detector()
# win = dlib.image_window()


stop_frame = 250


class Dlib_Find_Candidate_Object_Locations(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{389E2AAF-1CC8-46C8-ACD0-55E0C4D7DB56}'
    f_version = 1

    __PARAMS = {
        'threshold_limit': 4,
        'squares_count': 10,
        'roll_frames_count': 5,
        'min_size': 0.1,
    }

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = False

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        import dlib

        value = 0
        change = 0

        gray = image[:height * width].reshape([height, width])

        dets = []
        dlib.find_candidate_object_locations(gray, dets, min_size=int(height * width * self.f_params['min_size']))

        # image_file = '2009_004587.jpg'
        # img = dlib.load_rgb_image(image_file)
        # dlib.find_candidate_object_locations(img, dets, min_size=self.f_params['min_size'])
        # self.show_detected(img, height, width, dets)

        # print("number of rectangles found {}".format(len(dets)))
        # for k, d in enumerate(dets):
        #     print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
        #         k, d.left(), d.top(), d.right(), d.bottom()))

        if self.__SHOW and (len(dets) > 0):
            self.show_detected(gray, height, width, dets)

        rects = [[d.left(), d.top(), d.right() - d.left(), d.bottom() - d.top()] for d in dets]
        return self.process_rects(frame_index, rects, height, width, Items, value_last)


    def show_detected(self, image, height, width, dets):
        import dlib

        print("Number of candidates detected: {}".format(len(dets)))
        for i, d in enumerate(dets):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                i, d.left(), d.top(), d.right(), d.bottom()))

        rects = dets

        win = dlib.image_window()
        win.clear_overlay()
        win.set_image(image)
        win.add_overlay(rects)
        # dlib.hit_enter_to_continue()

