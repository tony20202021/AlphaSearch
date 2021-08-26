from Detectors import alpha_detector_squares_base

import numpy as np

# detector = dlib.get_frontal_face_detector()
# win = dlib.image_window()


stop_frame = 250

class Dlib_Cnn_Face_Detector(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{8FA9942A-0590-4178-BBAD-5D68B9F42A65}'
    f_version = 1

    __PARAMS = {
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,
        'upsample_count': 1,
    }

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

    def process_frame(self, frame_index, image, height, width, Item_FingerPrintOne, value_last):
        import dlib

        value = 0
        change = 0

        gray = image[:height * width].reshape([height, width])

        # cnn_face_detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
        # cnn_face_detector = dlib.cnn_face_detection_model_v1('mmod_rear_end_vehicle_detector.dat')
        cnn_face_detector = dlib.cnn_face_detection_model_v1('mmod_front_and_rear_end_vehicle_detector.dat')
        # cnn_face_detector = dlib.cnn_face_detection_model_v1('mmod_dog_hipsterizer.dat')

        # win = dlib.image_window()

        # img = dlib.load_rgb_image('Tom_Cruise_avp_2014_4.jpg')
        # dets = cnn_face_detector(img, 1)

        # The 1 in the second argument indicates that we should upsample the image
        # 1 time.  This will make everything bigger and allow us to detect more
        # faces.
        dets = cnn_face_detector(gray, self.f_params['upsample_count'])
        #     This detector returns a mmod_rectangles object. This object contains a list of mmod_rectangle objects.
        #     These objects can be accessed by simply iterating over the mmod_rectangles object
        #     The mmod_rectangle object has two member variables, a dlib.rectangle object, and a confidence score.

        if len(dets) > 0:
            self.show_detected(gray, height, width, dets)

        rects = [[d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom()] for d in dets]
        return self.process_rects(frame_index, rects, height, width, Item_FingerPrintOne, value_last)


    def show_detected(self, image, height, width, dets):
        import dlib

        print("Number of faces detected: {}".format(len(dets)))
        for i, d in enumerate(dets):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: {}".format(
                i, d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom(), d.confidence))

        rects = dlib.rectangles()
        rects.extend([d.rect for d in dets])

        win = dlib.image_window()
        win.clear_overlay()
        win.set_image(image)
        win.add_overlay(rects)
        # dlib.hit_enter_to_continue()

