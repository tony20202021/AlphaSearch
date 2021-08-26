from Detectors import alpha_detector_squares_base

import cv2

import numpy as np

class OpenCV_StructuredEdgeDetection(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{86500CEC-4C5F-4345-8741-18E58C41D97C}'
    f_version = 1
    __PARAMS = {
        'threshold_limit': 500,
        'squares_count': 10,
        'roll_frames_count': 5,
        'orimap': False,
        'threshold': 0.1,
    }
    __SHOW = None
    edge_detection = None

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = False
        self.edge_detection = cv2.ximgproc.createStructuredEdgeDetection('model.yml.gz')

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        gray = image[:height * width].reshape([height, width])

        gray3 = np.stack((gray, gray, gray), axis=-1)
        edges = self.edge_detection.detectEdges(np.float32(gray3) / 255.0)

        if self.f_params['orimap']:
            orimap = self.edge_detection.computeOrientation(edges)
            edges = self.edge_detection.edgesNms(edges, orimap)

        # edge_boxes = cv2.ximgproc.createEdgeBoxes()
        # edge_boxes.setMaxBoxes(30)
        # # boxes       = edge_boxes.getBoundingBoxes(edges, orimap)
        # boxes, scores = edge_boxes.getBoundingBoxes(edges, orimap)

        if self.__SHOW:
            self.show_detected(gray, height, width, edges)

        return self.process_pixels(frame_index, edges, self.f_params['threshold'] * edges.max(), height, width, Items, value_last)


    def show_detected(self, image, height, width, edges):
        # gray = image
        # gray3 = np.stack((gray, gray, gray), axis=-1)

        # if len(boxes) > 0:
        #     boxes_scores = zip(boxes, scores)
        #     for b_s in boxes_scores:
        #         box = b_s[0]
        #         x, y, w, h = box
        #         cv2.rectangle(gray3, (x, y), (x+w, y+h), (0, 255, 0), 1, cv2.LINE_AA)
        #         score = b_s[1][0]
        #         cv2.putText(gray3, "{:.2f}".format(score), (x, y), cv2.FONT_HERSHEY_PLAIN, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        #         # print("Box at (x,y)=({:d},{:d}); score={:f}".format(x, y, score))

        # cv2.destroyAllWindows()
        cv2.imshow("show", edges)
        cv2.waitKey(1)


# import cv2 as cv
# import numpy as np
# import sys
#
# if __name__ == '__main__':
#     print(__doc__)
#
#     model = sys.argv[1]
#     im = cv.imread(sys.argv[2])
#
#     edge_detection = cv.ximgproc.createStructuredEdgeDetection(model)
#     rgb_im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
#     edges = edge_detection.detectEdges(np.float32(rgb_im) / 255.0)
#
#     orimap = edge_detection.computeOrientation(edges)
#     edges = edge_detection.edgesNms(edges, orimap)
#
#     edge_boxes = cv.ximgproc.createEdgeBoxes()
#     edge_boxes.setMaxBoxes(30)
#     boxes = edge_boxes.getBoundingBoxes(edges, orimap)
#     boxes, scores = edge_boxes.getBoundingBoxes(edges, orimap)
#
#     if len(boxes) > 0:
#         boxes_scores = zip(boxes, scores)
#         for b_s in boxes_scores:
#             box = b_s[0]
#             x, y, w, h = box
#             cv.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 1, cv.LINE_AA)
#             score = b_s[1][0]
#             cv.putText(im, "{:.2f}".format(score), (x, y), cv.FONT_HERSHEY_PLAIN, 0.8, (255, 255, 255), 1, cv.LINE_AA)
#             print("Box at (x,y)=({:d},{:d}); score={:f}".format(x, y, score))
#
#     cv.imshow("edges", edges)
#     cv.imshow("edgeboxes", im)
#     cv.waitKey(0)
#     cv.destroyAllWindows()

