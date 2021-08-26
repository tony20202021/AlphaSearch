from Detectors.Dlib import alpha_dlib_cnn_face_detector
from Detectors.Dlib import alpha_dlib_frontal_face_detector
from Detectors.Dlib import alpha_dlib_find_candidate_object_locations

detectors_all = [
        alpha_dlib_cnn_face_detector.Dlib_Cnn_Face_Detector(),
        alpha_dlib_frontal_face_detector.Dlib_Frontal_Face_Detector(),
        alpha_dlib_find_candidate_object_locations.Dlib_Find_Candidate_Object_Locations(),
        ]

def get_all_detectors():
    return detectors_all

