from Detectors import alpha_detector_squares_base

import cv2

import numpy as np

class OpenCV_TEST(alpha_detector_squares_base.Detector_Squares_Base):
    f_id = '{47787A1F-8F87-4624-93EF-9EF41D65289D}'
    f_version = 1
    __PARAMS = {
        'threshold_limit': 20,
        'squares_count': 10,
        'roll_frames_count': 5,

        'HessianThreshold': 400, #50000
        'Upright': True,
        'Extended': True,
    }
    __SHOW = None

    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params
        self.__SHOW = True

    def process_frame(self, frame_index, image, height, width, Items, value_last):
        gray = image[:height * width].reshape([height, width])



        # surf = cv2.xfeatures2d.SURF_create(self.f_params['HessianThreshold'])
        # # surf.setHessianThreshold(50000)
        # surf.setUpright(self.f_params['Upright'])
        # self.f_params['Extended']
        # Finally we check the descriptor size and change it to 128 if it is only 64-dim.
        #
        # # Find size of descriptor
        # >>> print( surf.descriptorSize() )
        # 64
        # # That means flag, "extended" is False.
        # >>> surf.getExtended()
        #  False
        # # So we make it to True to get 128-dim descriptors.
        # >>> surf.setExtended(True)
        # >>> kp, des = surf.detectAndCompute(img,None)
        # >>> print( surf.descriptorSize() )
        # 128
        # >>> print( des.shape )
        # (47, 128)
        # key_points, des = surf.detectAndCompute(gray, None)
        # key_points = surf.detect(gray, None)


        # lsd = cv2.LineSegmentDetector()
        # lines = lsd.detect(gray)
        #
        # if (lines is None):
        #     points = []
        # else:
        #     points = []


        # erc1 = cv2.text.loadClassifierNM1('trained_classifierNM1.xml')
        # er1 = cv2.text.createERFilterNM1(erc1)
        #
        # erc2 = cv2.text.loadClassifierNM2('trained_classifierNM2.xml')
        # er2 = cv2.text.createERFilterNM2(erc2)
        #
        # regions = cv2.text.detectRegions(gray, er1, er2)
        #
        # if self.__SHOW and (regions is not None):
        #     self.show_detected(gray, height, width, regions)


        # textSpotter = cv2.text.TextDetectorCNN_create("textbox.prototxt", "TextBoxes_icdar13.caffemodel")
        # gray3 = np.stack((gray, gray, gray), axis=-1)
        # rects, outProbs = textSpotter.detect(gray3)
        # if self.__SHOW and (rects is not None):
        #     self.show_detected(gray, height, width, rects, outProbs)

        # gs = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
        # gray3 = np.stack((gray, gray, gray), axis=-1)
        # gs.setBaseImage(gray3)
        # # if (sys.argv[2][0] == 's'):
        # gs.switchToSingleStrategy()
        # # elif (sys.argv[2][0] == 'f'):
        # #     gs.switchToSelectiveSearchFast()
        # # elif (sys.argv[2][0] == 'q'):
        # #     gs.switchToSelectiveSearchQuality()
        # # else:
        # #     print(__doc__)
        # #     sys.exit(1)
        # rects = gs.process()

        # gray3 = np.stack((gray, gray, gray), axis=-1)
        # channels = cv2.text.computeNMChannels(gray3)
        # cn = len(channels)-1
        # for c in range(0,cn):
        #     channels.append((255-channels[c]))
        # for channel in channels:
        #     erc1 = cv2.text.loadClassifierNM1('trained_classifierNM1.xml')
        #     er1 = cv2.text.createERFilterNM1(erc1,16,0.00015,0.13,0.2,True,0.1)
        #     erc2 = cv2.text.loadClassifierNM2('trained_classifierNM2.xml')
        #     er2 = cv2.text.createERFilterNM2(erc2,0.5)
        #     regions = cv2.text.detectRegions(channel,er1,er2)
        #     # rects = cv2.text.erGrouping(gray3,channel,[r.tolist() for r in regions])
        #     # rects = cv2.text.erGrouping(gray3,channel,[x.tolist() for x in regions], cv2.text.ERGROUPING_ORIENTATION_ANY,'trained_classifier_erGrouping.xml',0.5)
        #     if (regions is not None):
        #         rects = [cv2.boundingRect(p.reshape(-1, 1, 2)) for p in regions]
        #     else:
        #         rects = []
        #     if self.__SHOW and (regions is not None):
        #         self.show_detected(gray, height, width, rects)

        orb = cv2.ORB_create()
        # find the keypoints with ORB
        kp = orb.detect(gray, None)
        # compute the descriptors with ORB
        # kp, des = orb.compute(gray, kp)
        if self.__SHOW and (kp is not None) and (len(kp) > 0):
            self.show_detected(gray, height, width, kp)

        points = []

        return self.process_points(frame_index, points, height, width, Items, value_last)


    def show_detected(self, image, height, width, kp):
        gray = image
        gray3 = np.stack((gray, gray, gray), axis=-1)

        # rects = [cv2.boundingRect(p.reshape(-1, 1, 2)) for p in regions]
        # for rect in rects:
        #   cv2.rectangle(gray3, rect[0:2], (rect[0]+rect[2],rect[1]+rect[3]), (0, 0, 0), 2)
        # for rect in rects:
        #   cv2.rectangle(gray3, rect[0:2], (rect[0]+rect[2],rect[1]+rect[3]), (255, 255, 255), 1)

        # thres = 0.6
        # for r in range(np.shape(rects)[0]):
        #     if outProbs[r] > thres:
        #         rect = rects[r]
        #         cv2.rectangle(gray3, (rect[0],rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 2)

        # for r in range(0,np.shape(rects)[0]):
        #     rect = rects[r]
        #     cv2.rectangle(gray3, (rect[0],rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (0, 0, 0), 2)
        #     cv2.rectangle(gray3, (rect[0],rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (255, 255, 255), 1)

        gray3 = cv2.drawKeypoints(gray3, kp, None, color=(0,255,0), flags=0)

        # cv2.destroyAllWindows()
        cv2.imshow("show", gray3)
        cv2.waitKey(1)



# >>> img = cv.imread('fly.png',0)
# # Create SURF object. You can specify params here or later.
# # Here I set Hessian Threshold to 400
# >>> surf = cv.xfeatures2d.SURF_create(400)
# # Find keypoints and descriptors directly
# >>> kp, des = surf.detectAndCompute(img,None)
# >>> len(kp)
#  699
# 1199 keypoints is too much to show in a picture. We reduce it to some 50 to draw it on an image. While matching, we may need all those features, but not now. So we increase the Hessian Threshold.
#
# # Check present Hessian threshold
# >>> print( surf.getHessianThreshold() )
# 400.0
# # We set it to some 50000. Remember, it is just for representing in picture.
# # In actual cases, it is better to have a value 300-500
# >>> surf.setHessianThreshold(50000)
# # Again compute keypoints and check its number.
# >>> kp, des = surf.detectAndCompute(img,None)
# >>> print( len(kp) )
# 47
# It is less than 50. Let's draw it on the image.
#
# >>> img2 = cv.drawKeypoints(img,kp,None,(255,0,0),4)
# >>> plt.imshow(img2),plt.show()
# See the result below. You can see that SURF is more like a blob detector. It detects the white blobs on wings of butterfly. You can test it with other images.
#
# surf_kp1.jpg
# image
# Now I want to apply U-SURF, so that it won't find the orientation.
#
# # Check upright flag, if it False, set it to True
# >>> print( surf.getUpright() )
# False
# >>> surf.setUpright(True)
# # Recompute the feature points and draw it
# >>> kp = surf.detect(img,None)
# >>> img2 = cv.drawKeypoints(img,kp,None,(255,0,0),4)
# >>> plt.imshow(img2),plt.show()
# See the results below. All the orientations are shown in same direction. It is faster than previous. If you are working on cases where orientation is not a problem (like panorama stitching) etc, this is better.
#
# surf_kp2.jpg
# image
# Finally we check the descriptor size and change it to 128 if it is only 64-dim.
#
# # Find size of descriptor
# >>> print( surf.descriptorSize() )
# 64
# # That means flag, "extended" is False.
# >>> surf.getExtended()
#  False
# # So we make it to True to get 128-dim descriptors.
# >>> surf.setExtended(True)
# >>> kp, des = surf.detectAndCompute(img,None)
# >>> print( surf.descriptorSize() )
# 128
# >>> print( des.shape )
# (47, 128)


