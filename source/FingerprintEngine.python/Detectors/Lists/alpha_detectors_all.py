from Detectors.Lists import alpha_open_cv_classifiers_all
from Detectors.Lists import alpha_detector_change_luma_all
from Detectors.Lists import alpha_dlib_all
from Detectors.OpenCV import alpha_open_cv_contour
from Detectors.OpenCV import alpha_open_cv_lines_slow
from Detectors.OpenCV import alpha_open_cv_lines_fast
from Detectors.OpenCV import alpha_open_cv_circles
from Detectors.OpenCV import alpha_open_cv_corners
from Detectors.OpenCV import alpha_open_cv_goodFeaturesToTrack
from Detectors.OpenCV import alpha_open_cv_SIFT
from Detectors.OpenCV import alpha_open_cv_TEST
from Detectors.OpenCV import alpha_open_cv_FastFeatureDetector
from Detectors.OpenCV import alpha_open_cv_text
from Detectors.OpenCV import alpha_open_cv_TextDetectorCNN
from Detectors.OpenCV import alpha_open_cv_StructuredEdgeDetection
from Detectors.OpenCV import alpha_open_cv_SelectiveSearchSegmentation
from Detectors.OpenCV import alpha_open_cv_text_computeNMChannels
from Detectors.OpenCV import alpha_open_cv_ORB


detectors = {}

for d in alpha_detector_change_luma_all.get_all_detectors():
    if d is not None:
        detectors[d.__class__.__name__] = {'detector': d, 'last': [None], 'xml_item': None}

# for d in alpha_open_cv_classifiers_all.get_all_detectors():
#     if d is not None:
#         detectors[d.__class__.__name__] = {'detector': d, 'last': [None], 'xml_item': None}

# detectors['OpenCV_Contour'] = {'detector': alpha_open_cv_contour.OpenCV_Contour(), 'last': [None], 'xml_item': None}

# detectors['OpenCV_Pedestrian'] = {'detector': alpha_open_cv_pedestrian.OpenCV_Pedestrian(), 'last': [None], 'xml_item': None}

# detectors['OpenCV_Lines_Slow'] = {'detector': alpha_open_cv_lines_slow.OpenCV_Lines_Slow(), 'last': [None], 'xml_item': None}
# detectors['OpenCV_Lines_Fast'] = {'detector': alpha_open_cv_lines_fast.OpenCV_Lines_Fast(), 'last': [None], 'xml_item': None}
# detectors['OpenCV_Circles'] = {'detector': alpha_open_cv_circles.OpenCV_Circles(), 'last': [None], 'xml_item': None}
# detectors['OpenCV_Corners_Harris'] = {'detector': alpha_open_cv_corners.OpenCV_Corners_Harris(), 'last': [None], 'xml_item': None}
# detectors['OpenCV_Corners_MinEigenVal'] = {'detector': alpha_open_cv_corners.OpenCV_Corners_MinEigenVal(), 'last': [None], 'xml_item': None}
# detectors['OpenCV_goodFeaturesToTrack'] = {'detector': alpha_open_cv_goodFeaturesToTrack.OpenCV_goodFeaturesToTrack(), 'last': [None], 'xml_item': None}
# detectors['OpenCV_SIFT'] = {'detector': alpha_open_cv_SIFT.OpenCV_SIFT(), 'last': [None], 'xml_item': None}
# detectors['OpenCV_FastFeatureDetector'] = {'detector': alpha_open_cv_FastFeatureDetector.OpenCV_FastFeatureDetector(), 'last': [None], 'xml_item': None}
# detectors['OpenCV_text'] = {'detector': alpha_open_cv_text.OpenCV_text(), 'last': [None], 'xml_item': None}
# detectors['OpenCV_TextDetectorCNN'] = {'detector': alpha_open_cv_TextDetectorCNN.OpenCV_TextDetectorCNN(), 'last': [None], 'xml_item': None}
# detectors['OpenCV_StructuredEdgeDetection'] = {'detector': alpha_open_cv_StructuredEdgeDetection.OpenCV_StructuredEdgeDetection(), 'last': [None], 'xml_item': None}
# detectors['OpenCV_SelectiveSearchSegmentation'] = {'detector': alpha_open_cv_SelectiveSearchSegmentation.OpenCV_SelectiveSearchSegmentation(), 'last': [None], 'xml_item': None}
# detectors['OpenCV_text_computeNMChannels'] = {'detector': alpha_open_cv_text_computeNMChannels.OpenCV_text_computeNMChannels(), 'last': [None], 'xml_item': None}

detectors['OpenCV_ORB'] = {'detector': alpha_open_cv_ORB.OpenCV_ORB(), 'last': [None], 'xml_item': None}

# detectors['OpenCV_TEST'] = {'detector': alpha_open_cv_TEST.OpenCV_TEST(), 'last': [None], 'xml_item': None}


# for d in alpha_dlib_all.get_all_detectors():
#     if d is not None:
#         detectors[d.__class__.__name__] = {'detector': d, 'last': [None], 'xml_item': None}

def get_all_detectors():
    return detectors


def get_all_finger_prints():
    result = {}
    for detector_key in detectors:
        for finger_print in detectors[detector_key]['detector'].get_finger_prints():
            result[finger_print['finger_print_name']] = finger_print
    return result

