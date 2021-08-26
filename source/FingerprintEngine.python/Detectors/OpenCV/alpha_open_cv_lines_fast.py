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

class OpenCV_Lines_Fast(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{7737777D-ECF1-47CC-BB43-966829E4A2F2}'
    f_version = 1

    __PARAMS = {
        'threshold_limit': 3,
        'squares_count': 10,
        'roll_frames_count': 5,
        'threshold1': 50,
        'threshold2': 150,
        'apertureSize': 3,
        'rho': 1,
        'theta': np.pi/180,
        'threshold': 100,
        'minLineLength': 100,
        'maxLineGap': 10,
    }

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = False

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        value = 0
        change = 0

        gray = image[:height * width].reshape([height, width])

        edges = cv2.Canny(gray, self.f_params['threshold1'], self.f_params['threshold2'], apertureSize=self.f_params['apertureSize'])
        lines = cv2.HoughLinesP(edges, self.f_params['rho'], self.f_params['theta'], self.f_params['threshold'], minLineLength=self.f_params['minLineLength'], maxLineGap=self.f_params['maxLineGap'])

        rects = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                rects.append([max(0, min(x1, x2)), max(0, min(y1, y2)), min(width, abs(x2-x1)), min(height, abs((y2-y1)))])

            if self.__SHOW and (len(lines) > 0):
                self.show_detected(gray, height, width, lines)

        return self.process_rects(frame_index, rects, height, width, Items, value_last)

    def show_detected(self, image, height, width, lines):
        gray = image
        gray3 = np.stack((gray, gray, gray), axis=-1)

        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(gray3, (x1, y1), (x2, y2), (0, 0, 255), 2)

        cv2.imshow("show", gray3)
        cv2.waitKey(500)
        cv2.destroyAllWindows()

# import cv2 as cv
# import numpy as np
# img = cv.imread(cv.samples.findFile('sudoku.png'))
# gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# edges = cv.Canny(gray,50,150,apertureSize = 3)
# lines = cv.HoughLinesP(edges,1,np.pi/180,100,minLineLength=100,maxLineGap=10)
# for line in lines:
#     x1,y1,x2,y2 = line[0]
#     cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
# cv.imwrite('houghlines5.jpg',img)