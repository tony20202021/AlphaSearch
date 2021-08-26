from Detectors import alpha_detector_change_luma_base


class Change_Luma_0_05(alpha_detector_change_luma_base.Change_Luma_Base):
    __PARAMS = {
        'diff_threshold_sum': 0.05,
        'use_roll_64': True,
        'use_diff_exact': True,
    }
    f_id = '{1FE62675-00FA-4D70-8F2D-0597CD9797F0}'
    f_version = 7

    def __init__(self, a_params=__PARAMS):
        super().__init__(a_params)

class Change_Luma_0_1(alpha_detector_change_luma_base.Change_Luma_Base):
    __PARAMS = {
        'diff_threshold_sum': 0.1,
        'use_roll_64': True,
        'use_diff_exact': True,
    }
    f_id = '{3D417D69-F352-4C40-AB24-641195AE2F6B}'
    f_version = 7

    def __init__(self, a_params=__PARAMS):
        super().__init__(a_params)

class Change_Luma_0_2(alpha_detector_change_luma_base.Change_Luma_Base):
    __PARAMS = {
        'diff_threshold_sum': 0.2,
        'use_roll_64': True,
        'use_diff_exact': True,
    }
    f_id = '{B41370C0-CC0C-4058-BAD1-045284B36A4F}'
    f_version = 7

    def __init__(self, a_params=__PARAMS):
        super().__init__(a_params)

class Change_Luma_0_05_roll_luma(alpha_detector_change_luma_base.Change_Luma_Base):
    __PARAMS = {
        'diff_threshold_sum': 0.05,
        'use_roll_64': True,
        'use_diff_exact': True,
        'use_roll_frames_luma': True,
        'roll_frames_count': 3,
    }
    f_id = '{30E9B491-6F79-49B1-95D0-0636F7AB3DD9}'
    f_version = 6

    def __init__(self, a_params=__PARAMS):
        super().__init__(a_params)


class Change_Luma_0_1_roll_luma(alpha_detector_change_luma_base.Change_Luma_Base):
    __PARAMS = {
        'diff_threshold_sum': 0.1,
        'use_roll_64': True,
        'use_diff_exact': True,
        'use_roll_frames_luma': True,
        'roll_frames_count': 3,
    }
    f_id = '{30E9B491-6F79-49B1-95D0-0636F7AB3DD9}'
    f_version = 6

    def __init__(self, a_params=__PARAMS):
        super().__init__(a_params)


class Change_Luma_0_2_roll_luma(alpha_detector_change_luma_base.Change_Luma_Base):
    __PARAMS = {
        'diff_threshold_sum': 0.2,
        'use_roll_64': True,
        'use_diff_exact': True,

        'use_roll_frames_luma': True,
        'roll_frames_count': 1,
    }
    f_id = '{F370BE73-453B-443B-9E49-BDAD46665934}'
    f_version = 6

    def __init__(self, a_params=__PARAMS):
        super().__init__(a_params)


class Change_Luma_0_05_roll_diff(alpha_detector_change_luma_base.Change_Luma_Base):
    __PARAMS = {
        'diff_threshold_sum': 0.05,
        'use_roll_64': True,
        'use_diff_exact': True,

        'use_roll_frames_diff': True,
        'roll_frames_count': 3,
    }
    f_id = '{FD71F5A9-3C38-4F75-AA52-94E2935857E4}'
    f_version = 6

    def __init__(self, a_params=__PARAMS):
        super().__init__(a_params)


class Change_Luma_0_1_roll_diff(alpha_detector_change_luma_base.Change_Luma_Base):
    __PARAMS = {
        'diff_threshold_sum': 0.1,
        'use_roll_64': True,
        'use_diff_exact': True,

        'use_roll_frames_diff': True,
        'roll_frames_count': 3,
    }
    f_id = '{1516FCAF-1A5E-4A28-B2A0-382DC3D8E75C}'
    f_version = 6

    def __init__(self, a_params=__PARAMS):
        super().__init__(a_params)


class Change_Luma_0_2_roll_diff(alpha_detector_change_luma_base.Change_Luma_Base):
    __PARAMS = {
        'diff_threshold_sum': 0.2,
        'use_roll_64': True,
        'use_diff_exact': True,

        'use_roll_frames_diff': True,
        'roll_frames_count': 3,
    }
    f_id = '{86C2CC57-1FEC-4EC5-A47B-8E6D36B45C83}'
    f_version = 6

    def __init__(self, a_params=__PARAMS):
        super().__init__(a_params)


class Change_Luma_0_05_roll_change(alpha_detector_change_luma_base.Change_Luma_Base):
    __PARAMS = {
        'diff_threshold_sum': 0.05,
        'use_roll_64': True,
        'use_diff_exact': True,

        'use_roll_frames_change': True,
        'roll_frames_count': 5,
    }
    f_id = '{34789871-FDE8-4443-9C24-F94FC2DBC16B}'
    f_version = 6

    def __init__(self, a_params=__PARAMS):
        super().__init__(a_params)


class Change_Luma_0_1_roll_change(alpha_detector_change_luma_base.Change_Luma_Base):
    __PARAMS = {
        'diff_threshold_sum': 0.1,
        'use_roll_64': True,
        'use_diff_exact': True,

        'use_roll_frames_change': True,
        'roll_frames_count': 3,
    }
    f_id = '{EE99D74C-127C-4F45-BB12-061F891F5953}'
    f_version = 6

    def __init__(self, a_params=__PARAMS):
        super().__init__(a_params)


class Change_Luma_0_2_roll_change(alpha_detector_change_luma_base.Change_Luma_Base):
    __PARAMS = {
        'diff_threshold_sum': 0.2,
        'use_roll_64': True,
        'use_diff_exact': True,

        'use_roll_frames_change': True,
        'roll_frames_count': 3,
    }
    f_id = '{E48F4219-7856-4327-9319-1BF7F738ED32}'
    f_version = 6

    def __init__(self, a_params=__PARAMS):
        super().__init__(a_params)


detectors_all = [
        Change_Luma_0_05(),
        # Change_Luma_0_1(),
        # Change_Luma_0_2(),
        # Change_Luma_0_05_roll_luma(),
        # Change_Luma_0_1_roll_luma(),
        # Change_Luma_0_2_roll_luma(),
        # Change_Luma_0_05_roll_diff(),
        # Change_Luma_0_1_roll_diff(),
        # Change_Luma_0_2_roll_diff(),
        # Change_Luma_0_05_roll_change(),
        # Change_Luma_0_1_roll_change(),
        # Change_Luma_0_2_roll_change(),
        ]

def get_all_detectors():
    return detectors_all

