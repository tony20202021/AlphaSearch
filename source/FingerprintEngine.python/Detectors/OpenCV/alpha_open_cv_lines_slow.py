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

class OpenCV_Lines_Slow(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{4EAD54A8-34E0-4F13-89A6-C25BD3DAAFDD}'
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
        'threshold': 200,
    }

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = False

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        value = 0
        change = 0

        gray = image[:height * width].reshape([height, width])

        edges = cv2.Canny(gray, self.f_params['threshold1'], self.f_params['threshold2'], apertureSize=self.f_params['apertureSize'])
        lines = cv2.HoughLines(edges, self.f_params['rho'], self.f_params['theta'], self.f_params['threshold'])

        rects = []
        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = max(0, int(x0 + 1000*(-b)))
                y1 = max(0, int(y0 + 1000*(a)))
                x2 = min(width, int(x0 - 1000*(-b)))
                y2 = min(height, int(y0 - 1000*(a)))
                rects.append([x1, y1, (x2-x1), (y2-y1)])

            if self.__SHOW and (len(lines) > 0):
                self.show_detected(gray, height, width, lines)

        return self.process_rects(frame_index, rects, height, width, Items, value_last)

    def show_detected(self, image, height, width, lines):
        gray = image
        gray3 = np.stack((gray, gray, gray), axis=-1)

        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = max(0, int(x0 + 1000 * (-b)))
            y1 = max(0, int(y0 + 1000 * (a)))
            x2 = min(width, int(x0 - 1000 * (-b)))
            y2 = min(height, int(y0 - 1000 * (a)))
            cv2.line(gray3, (x1, y1), (x2, y2), (0, 0, 255), 2)

        cv2.imshow("show", gray3)
        cv2.waitKey(500)
        cv2.destroyAllWindows()


# import cv2 as cv
# import numpy as np
# img = cv.imread(cv.samples.findFile('sudoku.png'))
# gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# edges = cv.Canny(gray,50,150,apertureSize = 3)
# lines = cv.HoughLines(edges,1,np.pi/180,200)
# for line in lines:
#     rho,theta = line[0]
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a*rho
#     y0 = b*rho
#     x1 = int(x0 + 1000*(-b))
#     y1 = int(y0 + 1000*(a))
#     x2 = int(x0 - 1000*(-b))
#     y2 = int(y0 - 1000*(a))
#     cv.line(img,(x1,y1),(x2,y2),(0,0,255),2)
# cv.imwrite('houghlines3.jpg',img)
