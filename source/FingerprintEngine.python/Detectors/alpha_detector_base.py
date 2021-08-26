class Detector_Base:
    __DIFF_MIN_SKIP = 10
    f_params = None
    f_id = '{00000000-0000-0000-0000-000000000000}'
    f_version = None

    def __init__(self, a_params=None):
        self.f_params = a_params

    def get_finger_prints(self):
        return [
            {'detector': self.__class__.__name__, 'finger_print_name': self.__class__.__name__, 'group': self.__class__.__name__},
        ]

    def process_init(self, video_info, Items):
        value_last = None
        return value_last

    def process_frame(self, frame_index, image, height, width, Item_FingerPrintOne, value_last):
        pass

    def post_process_default(self, video_info, Items):
        video_len_Frames = video_info['frames_actual']
        video_len_Seconds = video_info['duration']

        for finger_print_name in Items:
            Item_FingerPrintOne = Items[finger_print_name]

            result = {'Relative': {'Seconds': {'Post_Processed': [],
                                                 'Original': []},
                                    'Frames': {'Post_Processed': [],
                                                 'Original': []}},
                      'Absolute': {'Seconds': {'Post_Processed': [],
                                                'Original': []},
                                   'Frames': {'Post_Processed': [],
                                                'Original': []}},
                      }

            for Item_Absolute_Frames_Original in Item_FingerPrintOne.findall("./AsString/Absolute/Frames/Original"):
                if Item_Absolute_Frames_Original.text is not None:
                    result['Absolute']['Frames']['Original'] = [int(s) for s in Item_Absolute_Frames_Original.text.split(',')]

            for Item_Absolute_Frames_Post_Processed in Item_FingerPrintOne.findall("./AsString/Absolute/Frames/Post_Processed"):
                if Item_Absolute_Frames_Post_Processed.text is not None:
                    result['Absolute']['Frames']['Post_Processed'] = [int(s) for s in Item_Absolute_Frames_Post_Processed.text.split(',')]

            for i in range(0, len(result['Absolute']['Frames']['Original'])):
                if video_len_Frames > 0:
                    result['Absolute']['Seconds']['Original'].append(result['Absolute']['Frames']['Original'][i] * video_len_Seconds / video_len_Frames)
                else:
                    result['Absolute']['Seconds']['Original'].append(0)

                if i == 0:
                    result['Relative']['Frames']['Original'].append(result['Absolute']['Frames']['Original'][i])
                    result['Relative']['Seconds']['Original'].append(result['Absolute']['Seconds']['Original'][i])
                else:
                    result['Relative']['Frames']['Original'].append(result['Absolute']['Frames']['Original'][i] - result['Absolute']['Frames']['Original'][i - 1])
                    result['Relative']['Seconds']['Original'].append(result['Absolute']['Seconds']['Original'][i] - result['Absolute']['Seconds']['Original'][i - 1])

            for i in range(0, len(result['Absolute']['Frames']['Post_Processed'])):
                if video_len_Frames > 0:
                    result['Absolute']['Seconds']['Post_Processed'].append(result['Absolute']['Frames']['Post_Processed'][i] * video_len_Seconds / video_len_Frames)
                else:
                    result['Absolute']['Seconds']['Post_Processed'].append(0)

                if i == 0:
                    result['Relative']['Frames']['Post_Processed'].append(result['Absolute']['Frames']['Post_Processed'][i])
                    result['Relative']['Seconds']['Post_Processed'].append(result['Absolute']['Seconds']['Post_Processed'][i])
                else:
                    result['Relative']['Frames']['Post_Processed'].append(result['Absolute']['Frames']['Post_Processed'][i] - result['Absolute']['Frames']['Post_Processed'][i - 1])
                    result['Relative']['Seconds']['Post_Processed'].append(result['Absolute']['Seconds']['Post_Processed'][i] - result['Absolute']['Seconds']['Post_Processed'][i - 1])

            for Item_Relative_Seconds_Post_Processed in Item_FingerPrintOne.findall("./AsString/Relative/Seconds/Post_Processed"):
                Item_Relative_Seconds_Post_Processed.text = ','.join(['{:.2f}'.format(x) for x in result['Relative']['Seconds']['Post_Processed']])
            for Item_Relative_Seconds_Original in Item_FingerPrintOne.findall("./AsString/Relative/Seconds/Original"):
                Item_Relative_Seconds_Original.text = ','.join(['{:.2f}'.format(x) for x in result['Relative']['Seconds']['Original']])
            for Item_Relative_Frames_Post_Processed in Item_FingerPrintOne.findall("./AsString/Relative/Frames/Post_Processed"):
                Item_Relative_Frames_Post_Processed.text = ','.join([str(i) for i in result['Relative']['Frames']['Post_Processed']])
            for Item_Relative_Frames_Original in Item_FingerPrintOne.findall("./AsString/Relative/Frames/Original"):
                Item_Relative_Frames_Original.text = ','.join([str(i) for i in result['Relative']['Frames']['Original']])

            for Item_Absolute_Seconds_Post_Processed in Item_FingerPrintOne.findall("./AsString/Absolute/Seconds/Post_Processed"):
                Item_Absolute_Seconds_Post_Processed.text = ','.join(['{:.2f}'.format(x) for x in result['Absolute']['Seconds']['Post_Processed']])
            for Item_Absolute_Seconds_Original in Item_FingerPrintOne.findall("./AsString/Absolute/Seconds/Original"):
                Item_Absolute_Seconds_Original.text = ','.join(['{:.2f}'.format(x) for x in result['Absolute']['Seconds']['Original']])

    def post_process_min_step(self, video_info, Items):
        for finger_print_name in Items:
            Item_FingerPrintOne = Items[finger_print_name]
            if (self.f_params is None) or ('diff_min_skip' not in self.f_params):
                diff_min_skip = self.__DIFF_MIN_SKIP
            else:
                diff_min_skip = self.f_params['diff_min_skip']

            for Item_Absolute_Frames_Original in Item_FingerPrintOne.findall("./AsString/Absolute/Frames/Original"):
                if Item_Absolute_Frames_Original.text is not None:
                    original = [int(s) for s in Item_Absolute_Frames_Original.text.split(',')]
                    post_processed = []
                    for i in range(0, len(original)):
                        if i == 0:
                            post_processed.append(original[i])
                        else:
                            if abs(original[i] - original[i-1]) > diff_min_skip:
                                post_processed.append(original[i])
                    for Item_Absolute_Frames_Post_Processed in Item_FingerPrintOne.findall("./AsString/Absolute/Frames/Post_Processed"):
                        Item_Absolute_Frames_Post_Processed.text = ','.join(['{:d}'.format(i) for i in post_processed])

    def post_process(self, video_info, Items):
        self.post_process_min_step(video_info, Items)
        self.post_process_default(video_info, Items)

    def show_detected(self, image, height, width):
        pass
