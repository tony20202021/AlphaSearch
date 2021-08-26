from Detectors import alpha_detector_base

import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
import cv2
from matplotlib import pyplot as plt

class Change_Luma_Base(alpha_detector_base.Detector_Base):
    __PARAMS = {
        'diff_threshold_sum': 0.05,
        'diff_threshold_one': 0.02,
        'use_roll_64': False,
        'use_diff_exact': False,
        'use_roll_frames_luma': False,
        'use_roll_frames_diff': False,
        'use_roll_frames_change': False,
    }
    f_group = 'Change_Luma'
    __SHOW = None

    plot_figure = None
    plot_subplot = None
    plot_bar_current = None
    plot_bar_last = None
    plot_line_diff_all = None
    plot_line_diff_filtered = None

    # test - накапливаем массивы по всем кадрам
    # luma_all = np.empty((0, 64), int)
    # luma_diff_all = np.empty((0, 64), int)

    # график выбранной метрики по всем значениям
    # time_line_all = {'name': 'Change_Luma_Base', 'duration': 22, 'frames': 216, 'details': np.empty((0))}

    # test - показать графики по первым 6 кадрам
    # show_graphics.show_diff(bright_all, bright_diff_all)

    def __init__(self, a_params=None):
        if a_params is None:
            self.f_params = self.__PARAMS
        else:
            self.f_params = a_params
            for p in self.__PARAMS:
                if p not in self.f_params:
                    self.f_params[p] = self.__PARAMS[p]

        self.__SHOW = False


    def get_finger_prints(self):
        return [
            {'detector': self.__class__.__name__, 'finger_print_name': self.__class__.__name__, 'group': 'Change_Luma'},
            # {'detector': self.__class__.__name__, 'finger_print_name': self.__class__.__name__ + '.Blink', 'group': 'Change_Luma.Blink'},
        ]


    def process_frame(self, frame_index, image, height, width, items, value_last):
        value = None
        change = None
        luma_diff = None
        frame_index_for_save = frame_index

        image_flat = image[:height * width].reshape([height * width])
        gray = image[:height * width].reshape([height, width])

        # luma 256
        luma_current = np.bincount(image_flat, minlength=256)

        # rolling average 256 (3)
        luma_rolled = np.nan_to_num(pd.DataFrame(luma_current).rolling(3).mean().to_numpy(), nan=0)

        # quant 256 / 4 = 64
        luma_64 = np.nan_to_num([np.sum(b4).astype(int) for b4 in luma_rolled.reshape(64, 4)], nan=0)

        if self.f_params['use_roll_64']:
            # rolling average 64 (3)
            luma_64_rolled = np.nan_to_num(pd.DataFrame(luma_64).rolling(3).mean().to_numpy(), nan=0).reshape(64).astype(int)
            luma_final = luma_64_rolled
        else:
            luma_final = luma_64

        # diff -> change
        if self.f_params['use_roll_frames_luma']:
            assert(self.f_params['use_diff_exact'])

            # rolling average (last 10 frames)
            roll_frames_count = self.f_params['roll_frames_count']

            frame_index_for_save = None
            average = None
            last_list = None
            change = 0

            if value_last is None:
                last_list = [luma_final]
            else:
                last_list = np.append(value_last['last_list'], [luma_final], axis=0)

            last_list = last_list[-(roll_frames_count + 1 + roll_frames_count):]

            if len(last_list) >= (roll_frames_count + 1 + roll_frames_count):
                average = np.average(last_list, axis=0).astype(int)
                frame_index_for_save = frame_index - roll_frames_count
                if value_last['average'] is not None:
                    luma_diff = abs(average - value_last['average'])
                    change = np.sum(np.where(luma_diff > (height * width * self.f_params['diff_threshold_one']), luma_diff, 0)) / (2 * height * width)
                else:
                    change = 0
            else:
                average = None

            value = {'average': average, 'frame_index_for_save': frame_index_for_save, 'last_list': last_list}

        elif self.f_params['use_roll_frames_diff']:
            assert(self.f_params['use_diff_exact'])

            roll_frames_count = self.f_params['roll_frames_count']

            if value_last is None:
                luma_diff = None
                value = {'luma_final': luma_final, 'diff_average': None, 'diff_list': None}
                change = 0
            else:
                luma_diff = abs(luma_final - value_last['luma_final'])

                if value_last['diff_list'] is None:
                    diff_list = [luma_diff]
                else:
                    diff_list = np.append(value_last['diff_list'], [luma_diff], axis=0)
                    diff_list = diff_list[-roll_frames_count:]

                diff_average = np.average(diff_list, axis=0).astype(int)

                value = {'luma_final': luma_final, 'diff_average': diff_average, 'diff_list': diff_list}
                change = np.sum(np.where(diff_average > (height * width * self.f_params['diff_threshold_one']), diff_average, 0)) / (2 * height * width)

        elif self.f_params['use_roll_frames_change']:
            assert (self.f_params['use_diff_exact'])

            roll_frames_count = self.f_params['roll_frames_count']

            if value_last is None:
                value = {'luma_final': luma_final, 'change_average': None, 'change_list': None}
                change = 0
            else:
                luma_diff = abs(luma_final - value_last['luma_final'])
                luma_change = np.sum(np.where(luma_diff > (height * width * self.f_params['diff_threshold_one']), luma_diff, 0)) / (2 * height * width)

                if value_last['change_list'] is None:
                    change_list = [luma_change]
                else:
                    change_list = np.append(value_last['change_list'], [luma_change], axis=0)
                    change_list = change_list[-roll_frames_count:]

                change_average = np.average(change_list, axis=0).astype(float)

                value = {'luma_final': luma_final, 'change_average': change_average, 'change_list': change_list}
                change = change_average

        elif self.f_params['use_diff_exact']:
            if value_last is None:
                change = 0
            else:
                luma_diff = abs(luma_final - value_last['luma_final'])
                change = np.sum(np.where(luma_diff > (height * width * self.f_params['diff_threshold_one']), luma_diff, 0)) / (2 * height * width)

            value = {'luma_final': luma_final}
        else:
            if value_last is None:
                change = 0
            else:
                luma_diff = np.array([], int)
                luma_diff = np.append(luma_diff, min(abs(luma_final[0] - value_last['luma_final'][0]), abs(luma_final[0] - value_last['luma_final'][0 + 1])))
                luma_diff = np.append(luma_diff, [min(abs(luma_final[index] - value_last['luma_final'][index - 1]), abs(luma_final[index] - value_last['luma_final'][index]), abs(luma_final[index] - value_last['luma_final'][index + 1])) for index in range(1, len(luma_final) - 1)])
                luma_diff = np.append(luma_diff, min(abs(luma_final[-1] - value_last['luma_final'][-1 - 1]), abs(luma_final[-1] - value_last['luma_final'][-1])))

                change = np.sum(np.where(luma_diff > (height * width * self.f_params['diff_threshold_one']), luma_diff, 0)) / (2 * height * width)

            value = {'luma_final': luma_final}

        is_change = (change > self.f_params['diff_threshold_sum'])

        for finger_print_name in items:
            if finger_print_name == self.__class__.__name__:
                if is_change:
                    # alpha_show_graphics.show_gray_cv(image, height, width, str(frame_index))

                    for Item_Details in items[finger_print_name].iter('Details'):
                        Item_Change = ET.SubElement(Item_Details, 'Change')
                        Item_Change.set('frame_index', str(frame_index_for_save))
                        Item_Change.set('value', 'histogram...')
                        Item_Change.set('change', str(change))
                        Item_Change.set('threshold', str(self.f_params['diff_threshold_sum']))
                        # Item_Change.set('count_nonzero', str(np.count_nonzero(luma_diff)))
                        # Item_Change.set('count_all', str(len(luma_diff)))
                        # Item_Change.set('nonzero_percent', str(np.count_nonzero(luma_diff) / len(luma_diff)))

                    for Item_AsString in items[finger_print_name].iter('AsString'):
                        for Item_Absolute in Item_AsString.iter('Absolute'):
                            for Item_Frames in Item_Absolute.iter('Frames'):
                                for Item_Original in Item_Frames.iter('Original'):
                                    if (Item_Original.text is None) or (Item_Original.text == ''):
                                        Item_Original.text = str(frame_index_for_save)
                                    else:
                                        Item_Original.text += ',' + str(frame_index_for_save)

            if finger_print_name == self.__class__.__name__ + '.Blink':
                if value_last is None:
                    count_not_changed = 0
                else:
                    count_not_changed = value_last['count_not_changed']
                last_luma_changed = (value_last is not None) and (value_last['luma_changed'])

                blink_started = False
                blink_finished = False

                if change > self.f_params['diff_threshold_sum']:
                    value['luma_changed'] = True
                    if last_luma_changed:
                        count_not_changed += 1
                    else:
                        blink_started = True
                else:
                    value['luma_changed'] = False
                    if last_luma_changed:
                        blink_finished = True
                    else:
                        count_not_changed += 1

                if blink_started or blink_finished:
                    for Item_Original in items[finger_print_name].findall("./AsString/Absolute/Frames/Original"):
                        if (Item_Original.text is None) or (Item_Original.text == ''):
                            Item_Original.text = str(frame_index)
                        else:
                            Item_Original.text += ',' + str(frame_index)
                    count_not_changed = 1

                value['count_not_changed'] = count_not_changed

        # self.time_line_all['details'] = np.append(self.time_line_all['details'], {'frame_index': frame_index, 'value': value, 'change': change})

        # self.luma_all = np.append(self.luma_all, [luma_final], axis=0)
        # if luma_diff is None:
        #     self.luma_diff_all = np.append(self.luma_diff_all, [np.zeros(64)], axis=0)
        # else:
        #     self.luma_diff_all = np.append(self.luma_diff_all, [luma_diff], axis=0)

        if self.__SHOW:
            self.show_detected(gray,
                               frame_index, frame_index_for_save,
                               height, width,
                               is_change, change, luma_diff, value, value_last,
                               )

        result = {'value' : value,
                'change' : change,
                'value_for_save' : value,
        }

        return result

    def post_process(self, video_info, items):
        # test - показать графики по первым 6 кадрам
        # alpha_show_graphics.show_diff(self.luma_all, self.luma_diff_all)

        # график выбранной метрики по всем значениям
        # alpha_show_graphics.show_time_line(self.time_line_all, 22)

        super().post_process_min_step(video_info, items)
        super().post_process_default(video_info, items)


    def putTextEx(self, img, text, org, fontFace, fontScale, color_back, color_front, thickness_back, thickness_front, lineType=None, bottomLeftOrigin=None):
        cv2.putText(img, text, org, fontFace, fontScale,
                    color_back, thickness_back)
        cv2.putText(img, text, org, fontFace, fontScale,
                    color_front, thickness_front)


    def show_detected(self,
                      gray,
                      frame_index, frame_index_for_save,
                      height, width,
                      is_change, change, luma_diff, value, value_last,
                      ):
        gray3 = np.stack((gray, gray, gray), axis=-1)

        fontScale = max(0.8, min(3.0, round(min(height, width) / 400, 1)))

        self.putTextEx(gray3,
                    "frame_index={}".format(frame_index),
                    (int(0.3 * width), int(0.12 * height)),
                    cv2.FONT_HERSHEY_PLAIN, fontScale,
                    (255, 255, 255), (0, 0, 0),
                    3, 1)

        self.putTextEx(gray3,
                    "frame_index_for_save={}".format(frame_index_for_save),
                    (int(0.3 * width), int(0.22 * height)),
                    cv2.FONT_HERSHEY_PLAIN, fontScale,
                    (255, 255, 255), (0, 0, 0),
                    3, 1)

        if is_change:
            self.putTextEx(gray3,
                           "change",
                           (int(0.1 * width), int(0.1 * height)),
                           cv2.FONT_HERSHEY_PLAIN, fontScale,
                           (255, 255, 255),
                           (0, 0, 255),
                           10, 5)

        self.putTextEx(gray3,
                       "change   = {} / {}".format("{:.2f}".format(change),
                                                                 self.f_params['diff_threshold_sum'],
                                                                 ),
                        (0, int(0.32 * height)),
                        cv2.FONT_HERSHEY_PLAIN, fontScale,
                        (0, 0, 255) if is_change else (255, 255, 255),
                        (0, 0, 0) if is_change else (0, 0, 0),
                        3, 1)

        cv2.imshow("show", gray3)
        cv2.waitKey(1)

        luma_final = value['luma_final']
        value_last_luma_final = value_last.get('luma_final', None) if value_last is not None else None
        x_count = 64

        if self.plot_figure is None:
            self.plot_figure = plt.figure(figsize=(7, 2))
        if self.plot_subplot is None:
            self.plot_subplot = self.plot_figure.add_subplot(111)
        if self.plot_bar_last is None:
            self.plot_bar_last = self.plot_subplot.bar(np.arange(x_count), np.arange(x_count), width=0.4, color="orange")
        if self.plot_bar_current is None:
            self.plot_bar_current = self.plot_subplot.bar(np.arange(x_count) + 0.4, np.arange(x_count), width=0.4, color="blue")
        if self.plot_line_diff_all is None:
            self.plot_line_diff_all = self.plot_subplot.plot(np.arange(x_count), np.arange(x_count), linewidth=3, color="red")
        if self.plot_line_diff_filtered is None:
            self.plot_line_diff_filtered = self.plot_subplot.plot(np.arange(x_count), np.arange(x_count), linewidth=2, color="green")

        plt.xlim([0, x_count])
        plt.ylim([0, max(max(luma_final), 0 if value_last_luma_final is None else max(value_last_luma_final))])

        if value_last_luma_final is not None:
            for i in range(len(self.plot_bar_last.patches)):
                self.plot_bar_last[i].set_height(value_last_luma_final[i])
        for i in range(len(self.plot_bar_current.patches)):
            self.plot_bar_current[i].set_height(luma_final[i])
        if luma_diff is not None:
            self.plot_line_diff_all[0].set_ydata(luma_diff)
            self.plot_line_diff_filtered[0].set_ydata(np.where(luma_diff > (height * width * self.f_params['diff_threshold_one']), luma_diff, 0))

        plt.show(block=False)

        if is_change:
            # plt.pause(1.0)
            plt.pause(0.0001)
        else:
            plt.pause(0.0001)


