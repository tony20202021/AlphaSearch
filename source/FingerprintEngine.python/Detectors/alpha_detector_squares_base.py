from Detectors import alpha_detector_base
import numpy as np
import cv2
import xml.etree.ElementTree as ET

stop_frame = 250

class Detector_Squares_Base(alpha_detector_base.Detector_Base):
    f_params = None
    f_id = '{00000000-0000-0000-0000-000000000000}'
    f_version = None

    def __init__(self, a_params=None):
        self.f_params = a_params

    def get_finger_prints(self):
        return [
            {'detector': self.__class__.__name__, 'finger_print_name': self.__class__.__name__, 'group': self.__class__.__name__},
            {'detector': self.__class__.__name__, 'finger_print_name': self.__class__.__name__ + '.Squares', 'group': self.__class__.__name__},
        ]

    def process_rects(self, frame_index, rects, height, width, Items, value_last):
        squares = np.zeros((self.f_params['squares_count'], self.f_params['squares_count']), int)
        for r in rects:
            x = r[0]
            y = r[1]
            w = r[2]
            h = r[3]
            center = {
                'y': min(self.f_params['squares_count'] - 1, int((y + 0.5 * h) * self.f_params['squares_count'] / height)),
                'x': min(self.f_params['squares_count'] - 1, int((x + 0.5 * w) * self.f_params['squares_count'] / width))
            }
            area = int(h * w)

            squares[center['y'], center['x']] += 1

        sum0 = np.sum(squares)
        sum1 = len(rects)
        if (sum0 != sum1):
            squares = None

        return self.process_squares(frame_index, squares, height, width, Items, value_last)

    def process_points(self, frame_index, points, height, width, Items, value_last, is_binary):
        squares = np.zeros((self.f_params['squares_count'], self.f_params['squares_count']), int)
        for p in points:
            center = {
                'y': min(self.f_params['squares_count'] - 1, int(p['y'] * self.f_params['squares_count'] / height)),
                'x': min(self.f_params['squares_count'] - 1, int(p['x'] * self.f_params['squares_count'] / width))
            }
            if is_binary:
                squares[center['y'], center['x']] = 1
            else:
                squares[center['y'], center['x']] += 1

        if not is_binary:
            sum0 = np.sum(squares)
            sum1 = len(points)
            assert(sum0 == sum1)

        return self.process_squares(frame_index, squares, height, width, Items, value_last)

    def process_pixels(self, frame_index, pixels, threshold, height, width, Items, value_last):
        squares = [[(pixels[int(height * y / self.f_params['squares_count']):int(height * (y + 1) / self.f_params['squares_count']), int(width * x / self.f_params['squares_count']):int(width * (x + 1) / self.f_params['squares_count'])] > threshold).sum() for x in range(self.f_params['squares_count'])] for y in range(self.f_params['squares_count'])]
        sum0 = np.sum(squares)

        sum2 = len(np.where(pixels > threshold)[0])
        points2 = np.copy(pixels)
        points2[pixels > threshold] = 1
        points2[pixels <= threshold] = 0
        sum3 = np.sum(points2)
        if ((sum0 != sum2) or
            (sum2 != sum3) or
            (sum3 != sum0)):
            squares = None

        return self.process_squares(frame_index, squares, height, width, Items, value_last)

    def process_squares(self, frame_index, squares, height, width, Items, value_last):
        value = 0
        change = 0

        # rolling average (last N frames + current frame + N next frames)
        roll_frames_count = self.f_params['roll_frames_count']

        frame_index_for_save = None
        average = None
        last_list = None
        change_total = 0
        change_squares_sum_exact = 0
        change_squares_sum = 0
        change_squares_max = 0
        squares_diff_exact = None
        squares_diff_shifted = None

        if value_last is None:
            last_list = [squares]
        else:
            last_list = np.append(value_last['last_list'], [squares], axis=0)

        last_list = last_list[-(roll_frames_count + 1 + roll_frames_count):]

        if len(last_list) >= (roll_frames_count + 1 + roll_frames_count):
            average = np.average(last_list, axis=0).round().astype(int)

            frame_index_for_save = frame_index - roll_frames_count
            assert(frame_index_for_save >= 0)

            if (value_last is not None) and (value_last['average'] is not None):
                squares_shifted_m_y_m_x = np.roll(value_last['average'], 1, axis=0)
                squares_shifted_m_y_m_x[0, :] = squares_shifted_m_y_m_x[1, :]
                squares_shifted_m_y_m_x = np.roll(squares_shifted_m_y_m_x, 1, axis=1)
                squares_shifted_m_y_m_x[:, 0] = squares_shifted_m_y_m_x[:, 1]

                squares_shifted_m_y___x = np.roll(value_last['average'], 1, axis=0)
                squares_shifted_m_y___x[0, :] = squares_shifted_m_y___x[1, :]

                squares_shifted_m_y_p_x = np.roll(value_last['average'], 1, axis=0)
                squares_shifted_m_y_p_x[0, :] = squares_shifted_m_y_p_x[1, :]
                squares_shifted_m_y_p_x = np.roll(squares_shifted_m_y_p_x, -1, axis=1)
                squares_shifted_m_y_p_x[:, -1] = squares_shifted_m_y_p_x[:, -2]

                squares_shifted___y_m_x = np.roll(value_last['average'], 1, axis=1)
                squares_shifted___y_m_x[:, 0] = squares_shifted___y_m_x[:, 1]

                squares_shifted___y___x = np.copy(value_last['average'])

                squares_shifted___y_p_x = np.roll(value_last['average'], -1, axis=1)
                squares_shifted___y_p_x[:, -1] = squares_shifted___y_p_x[:, -2]

                squares_shifted_p_y_m_x = np.roll(value_last['average'], -1, axis=0)
                squares_shifted_p_y_m_x[-1, :] = squares_shifted_p_y_m_x[-2, :]
                squares_shifted_p_y_m_x = np.roll(squares_shifted_p_y_m_x, 1, axis=1)
                squares_shifted_p_y_m_x[:, 0] = squares_shifted_p_y_m_x[:, 1]

                squares_shifted_p_y___x = np.roll(value_last['average'], -1, axis=0)
                squares_shifted_p_y___x[-1, :] = squares_shifted_p_y___x[-2, :]

                squares_shifted_p_y_p_x = np.roll(value_last['average'], -1, axis=0)
                squares_shifted_p_y_p_x[-1, :] = squares_shifted_p_y_p_x[-2, :]
                squares_shifted_p_y_p_x = np.roll(squares_shifted_p_y_p_x, -1, axis=1)
                squares_shifted_p_y_p_x[:, -1] = squares_shifted_p_y_p_x[:, -2]

                squares_diff_shifted = [
                    abs(average - squares_shifted_m_y_m_x),
                    abs(average - squares_shifted_m_y___x),
                    abs(average - squares_shifted_m_y_p_x),
                    abs(average - squares_shifted___y_m_x),
                    abs(average - squares_shifted___y___x),
                    abs(average - squares_shifted___y_p_x),
                    abs(average - squares_shifted_p_y_m_x),
                    abs(average - squares_shifted_p_y___x),
                    abs(average - squares_shifted_p_y_p_x)
                ]
                squares_diff_shifted = np.min(squares_diff_shifted, axis=0)
                squares_diff_exact = abs(average - value_last['average'])

                change_squares_sum_exact = np.sum(squares_diff_exact)
                change_squares_sum = np.sum(squares_diff_shifted)
                change_squares_max = np.max(squares_diff_shifted)
                change_total = abs(np.sum(average) - np.sum(value_last['average']))
            else:
                change_total = 0
                change_squares_sum_exact = 0
                change_squares_sum = 0
                change_squares_max = 0
        else:
            average = None

        value = {'average': average, 'frame_index_for_save': frame_index_for_save, 'last_list': last_list}

        # diff
        threshold_limit_total       = None if value_last is None else None if value_last['average'] is None else np.sum(value_last['average']) * (self.f_params['threshold_limit_total']       if 'threshold_limit_total'       in self.f_params else self.f_params['threshold_limit'])
        threshold_limit_squares_max = None if value_last is None else None if value_last['average'] is None else np.sum(value_last['average']) * (self.f_params['threshold_limit_squares_max'] if 'threshold_limit_squares_max' in self.f_params else self.f_params['threshold_limit'])
        threshold_limit_squares_sum = None if value_last is None else None if value_last['average'] is None else np.sum(value_last['average']) * (self.f_params['threshold_limit_squares_sum'] if 'threshold_limit_squares_sum' in self.f_params else self.f_params['threshold_limit'])
        threshold_limit_squares_sum_exact = None if value_last is None else None if value_last['average'] is None else np.sum(value_last['average']) * (self.f_params['threshold_limit_squares_sum_exact'] if 'threshold_limit_squares_sum_exact' in self.f_params else self.f_params['threshold_limit'])

        is_change_total       = False if threshold_limit_total       is None else (change_total >= threshold_limit_total)
        is_change_squares_max = False if threshold_limit_squares_max is None else (change_squares_max >= threshold_limit_squares_max)
        is_change_squares_sum = False if threshold_limit_squares_sum is None else (change_squares_sum >= threshold_limit_squares_sum)
        is_change_squares_sum_exact = False if threshold_limit_squares_sum_exact is None else (change_squares_sum_exact >= threshold_limit_squares_sum_exact)

        for index, (key, Item_FingerPrintOne) in enumerate(Items.items()):
            if (((key == self.__class__.__name__) and is_change_total) or
                ((key == self.__class__.__name__ + '.Squares') and (is_change_total or is_change_squares_sum_exact or is_change_squares_sum or is_change_squares_max))):

                for Item_Details in Item_FingerPrintOne.iter('Details'):
                    Item_Change = ET.SubElement(Item_Details, 'Change')
                    Item_Change.set('frame_index', str(frame_index_for_save))
                    Item_Change.set('sum_objects', str(np.sum(squares)))
                    Item_Change.set('sum_objects_average', str(np.sum(average)))
                    Item_Change.set('change_total_average', str(change_total))
                    if (key == self.__class__.__name__ + '.Squares'):
                        Item_Change.set('change_squares_average', str(change_squares_sum))

                for Item_AsString in Item_FingerPrintOne.iter('AsString'):
                    for Item_Absolute in Item_AsString.iter('Absolute'):
                        for Item_Frames in Item_Absolute.iter('Frames'):
                            for Item_Original in Item_Frames.iter('Original'):
                                if (Item_Original.text is None) or (Item_Original.text == ''):
                                    Item_Original.text = str(frame_index_for_save)
                                else:
                                    Item_Original.text += ',' + str(frame_index_for_save)

            # print('frame {}:  change: {} -> {})'.format(frame_index, value_last, value))

        result = {'value' : value,
                'change' : change,
                'value_for_save' : value,
                'frame_index_for_save' : frame_index_for_save,
                'average' : average,
                'squares_diff_exact' : squares_diff_exact,
                'squares_diff_shifted' : squares_diff_shifted,
                'change_total' : change_total,
                'change_squares_sum_exact' : change_squares_sum_exact,
                'change_squares_sum' : change_squares_sum,
                'change_squares_max' : change_squares_max,
                'is_change_total' : is_change_total,
                'is_change_squares_sum_exact' : is_change_squares_sum_exact,
                'is_change_squares_sum' : is_change_squares_sum,
                'is_change_squares_max' : is_change_squares_max,
              }
        return result


    def putTextEx(self, img, text, org, fontFace, fontScale, color_back, color_front, thickness_back, thickness_front, lineType=None, bottomLeftOrigin=None):
        cv2.putText(img, text, org, fontFace, fontScale,
                    color_back, thickness_back)
        cv2.putText(img, text, org, fontFace, fontScale,
                    color_front, thickness_front)


    def show_detected(self, image,
                      frame_index, frame_index_for_save,
                      height, width,
                      value_last_average, squares_average, squares_diff_exact, squares_diff_shifted,
                      change_total, change_squares_sum_exact, change_squares_sum, change_squares_max,
                      is_change_total, is_change_squares_sum_exact, is_change_squares_sum, is_change_squares_max):
        gray3 = image

        fontScale = max(0.8, min(3.0, round(min(height, width) / 400, 1)))

        for y in range(self.f_params['squares_count']):
            cv2.line(gray3, (0, int(y * height / self.f_params['squares_count'])), (width - 1, int(y * height / self.f_params['squares_count'])), (255, 0, 0))
        for x in range(self.f_params['squares_count']):
            cv2.line(gray3, (int(x * width / self.f_params['squares_count']), 0), (int(x * width / self.f_params['squares_count']), height - 1), (255, 0, 0))

        if (squares_average is not None):
            for y in range(self.f_params['squares_count']):
                for x in range(self.f_params['squares_count']):
                    if (squares_diff_shifted is not None) and (squares_diff_shifted[y][x] != 0):
                        cv2.rectangle(gray3,
                                 (int(x * width / self.f_params['squares_count']) + 1,
                                  int(y * height / self.f_params['squares_count']) + 1),
                                 (int((x + 1) * width / self.f_params['squares_count']) - 1,
                                  int((y + 1) * height / self.f_params['squares_count']) - 1),
                                  (0, 0, 255)) #BGR

                    if ((squares_average[y][x] != 0) or \
                       ((squares_diff_exact is not None) and (squares_diff_exact[y][x] != 0)) or \
                       ((squares_diff_shifted is not None) and (squares_diff_shifted[y][x] != 0)) or \
                       ((value_last_average is not None) and (value_last_average[y][x] != 0))):
                        self.putTextEx(gray3,
                                "{}->{}".format(('(-)' if (value_last_average is None) else value_last_average[y][x]), squares_average[y][x]),
                                (int(x * width / self.f_params['squares_count']), int((y + 0.4) * height / self.f_params['squares_count'])),
                                cv2.FONT_HERSHEY_PLAIN, fontScale,
                                (0, 0, 0), (255, 255, 255),
                                3, 1)
                        self.putTextEx(gray3,
                                "e{}, s{}".format(('-' if (squares_diff_exact is None) else squares_diff_exact[y][x]), ('-' if (squares_diff_shifted is None) else squares_diff_shifted[y][x])),
                                (int(x * width / self.f_params['squares_count']), int((y + 0.7) * height / self.f_params['squares_count'])),
                                cv2.FONT_HERSHEY_PLAIN, fontScale,
                                (0, 0, 0), (255, 255, 255),
                                3, 1)

        self.putTextEx(gray3,
                    "frame_index={}".format(frame_index),
                    (0, int(0.12 * height)),
                    cv2.FONT_HERSHEY_PLAIN, fontScale,
                    (255, 255, 255), (0, 0, 0),
                    3, 1)

        self.putTextEx(gray3,
                    "for_save={}".format(frame_index_for_save),
                    (0, int(0.22 * height)),
                    cv2.FONT_HERSHEY_PLAIN, fontScale,
                    (255, 255, 255), (0, 0, 0),
                    3, 1)

        self.putTextEx(gray3,
                       "total          = {} / {} (limit={}*{} -> {})".format(change_total,
                                                                 None if value_last_average is None else "{:.2f}".format(self.f_params['threshold_limit_total'] * np.sum(value_last_average)),
                                                                 self.f_params['threshold_limit_total'],
                                                                 np.sum(value_last_average),
                                                                 np.sum(squares_average),
                                                                 ),
                        (0, int(0.32 * height)),
                        cv2.FONT_HERSHEY_PLAIN, fontScale,
                        (0, 0, 255) if is_change_total else (255, 255, 255),
                        (0, 0, 0) if is_change_total else (0, 0, 0),
                        3, 1)

        self.putTextEx(gray3,
                    "sum_exact = {}/{} (limit={}*{})".format(change_squares_sum_exact,
                                             None if value_last_average is None else "{:.2f}".format(self.f_params['threshold_limit_squares_sum_exact'] * np.sum(value_last_average)),
                                             self.f_params['threshold_limit_squares_sum_exact'],
                                             np.sum(value_last_average),
                                             ),
                    (0, int(0.42 * height)),
                    cv2.FONT_HERSHEY_PLAIN, fontScale,
                    (0, 0, 255) if is_change_squares_sum_exact else (255, 255, 255),
                    (0, 0, 0) if is_change_squares_sum_exact else (0, 0, 0),
                    3, 1)

        self.putTextEx(gray3,
                    "sum_shifted = {} / {} (limit={}*{} -> {})".format(change_squares_sum,
                                                                    None if value_last_average is None else "{:.2f}".format(self.f_params['threshold_limit_squares_sum'] * np.sum(value_last_average)),
                                                                    self.f_params['threshold_limit_squares_sum'],
                                                                    np.sum(value_last_average),
                                                                    np.sum(squares_average),
                                                                  ),
                    (0, int(0.52 * height)),
                    cv2.FONT_HERSHEY_PLAIN, fontScale,
                    (0, 0, 255) if is_change_squares_sum else (255, 255, 255),
                    (0, 0, 0) if is_change_squares_sum else (0, 0, 0),
                    3, 1)

        self.putTextEx(gray3,
                    "squares_max = {} / {} (limit={}*{} -> {})".format(change_squares_max,
                                                                    None if value_last_average is None else "{:.2f}".format(self.f_params['threshold_limit_squares_max'] * np.sum(value_last_average)),
                                                                    self.f_params['threshold_limit_squares_max'],
                                                                    np.sum(value_last_average),
                                                                    np.sum(squares_average),
                                                                    ),
                    (0, int(0.62 * height)),
                    cv2.FONT_HERSHEY_PLAIN, fontScale,
                    (0, 0, 255) if is_change_squares_max else (255, 255, 255),
                    (0, 0, 0) if is_change_squares_max else (0, 0, 0),
                    3, 1)

        # cv2.destroyAllWindows()
        cv2.namedWindow("show")
        cv2.setMouseCallback("show", self.mouse_callback)
        cv2.imshow("show", gray3)
        if is_change_total or is_change_squares_sum or is_change_squares_max or is_change_squares_sum_exact:
            cv2.waitKey(500)
        else:
            cv2.waitKey(1)


    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            pressed = True
        elif event == cv2.EVENT_LBUTTONUP:
            pressed = False
