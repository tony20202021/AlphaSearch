from Detectors.OpenCV import alpha_open_cv_classifier_base


class OpenCV_eye(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_eye.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{8AFC8A28-A00E-45A3-89CB-876C670633A9}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_eye_tree_eyeglasses(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_eye_tree_eyeglasses.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{519CA598-D679-4D3E-9C18-2ADAFCFDEF5A}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_frontalface_alt(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_frontalface_alt.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{FC38E35B-4092-4766-8D3B-1A42FC5ABE26}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_frontalface_alt_tree(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_frontalface_alt_tree.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{DC350B5E-93F1-45C3-BF98-98605B55AD26}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_frontalface_alt2(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_frontalface_alt2.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{3B0E8467-CA9A-4F98-935A-883F9108B90D}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_frontalcatface(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_frontalcatface.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{D9DDB3D4-A255-4576-8A0F-9108E537F897}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_frontalcatface_extended(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_frontalcatface_extended.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{0A913BCE-C8CB-4F10-B664-5798A78475C9}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_frontalface_default(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_frontalface_default.xml',
        'scaleFactor': 1.1,
        'minNeighbors': 5,
        'minSize': (10, 10),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{1604802A-023F-4044-8E9B-E9C25E8CEE5B}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_fullbody(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_fullbody.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{AD31AE40-C7C7-402E-ABF9-415B862E04ED}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_lefteye_2splits(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_lefteye_2splits.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,
    }

    f_id = '{E1AC2A6C-3C37-48BB-8DCD-A5B36215B4EC}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_licence_plate_rus_16stages(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_licence_plate_rus_16stages.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,
    }

    f_id = '{ED52A754-A3C4-4844-917C-26E89AB1099E}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_lowerbody(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_lowerbody.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{1C296FEF-BC46-49E1-94C5-527FE8369AA0}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_profileface(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_profileface.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{E4B005EE-2669-4C8B-8440-5161144BF6EA}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_righteye_2splits(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_righteye_2splits.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{A112195B-40BA-4001-8415-6AB149EB3C7A}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_russian_plate_number(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_russian_plate_number.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{F88A0378-2704-4867-B5E6-B09DD0EFB229}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_smile(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_smile.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,

    }
    f_id = '{B30B4DB6-F7B7-4E2A-9399-4A931CF216F0}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params

class OpenCV_upperbody(alpha_open_cv_classifier_base.OpenCV_Base):
    __PARAMS = {
        'config_file': 'haarcascade_upperbody.xml',
        'scaleFactor': 1.3,
        'minNeighbors': 10,
        'minSize': (75, 75),
        'threshold_limit': 1,
        'squares_count': 10,
        'roll_frames_count': 1,
    }
    f_id = '{581E757E-A2F5-446C-AC48-681C2288708B}'
    def __init__(self, a_params=__PARAMS):
        self.f_params = a_params


detectors_all = [                               #cats
        # OpenCV_eye(),                         #01:08 #01:17
        #
        # OpenCV_eye_tree_eyeglasses(),         #02:27 #01:54
        # OpenCV_frontalcatface(),              #01:43 #01:29
        # OpenCV_frontalcatface_extended(),     #02:07 #01:32
        # OpenCV_frontalface_alt(),             #02:44 #02:30
        # OpenCV_frontalface_alt_tree(),        #11:28 #
        # OpenCV_frontalface_alt2(),            #03:13 #
        # #
        # OpenCV_frontalface_default(),         #05:25 #
        # #
        # OpenCV_fullbody(),                    #02:14 #01:17
        OpenCV_lefteye_2splits(),             #01:52 #00:34 (1)
        # OpenCV_licence_plate_rus_16stages(),  #01:43 #00:26
        # OpenCV_lowerbody(),                   #02:29 #01:31
        # OpenCV_profileface(),                 #04:09 #
        # OpenCV_righteye_2splits(),            #02:20 #00:53
        # OpenCV_russian_plate_number(),        #02:18 #00:37
        # #
        # OpenCV_smile(),                       #04:35 #
        # OpenCV_upperbody(),                   #05:43 #02:51
        ]

def get_all_detectors():
    return detectors_all



#