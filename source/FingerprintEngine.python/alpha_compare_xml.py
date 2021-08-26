#coding: utf-8

from Detectors.Lists import alpha_detectors_all

import os
import pathlib
import xml.etree.ElementTree as ET
from dtw import *
from tabulate import tabulate
import numpy as np
from shapely.geometry import Polygon
import datetime

f_params = {
    'limit_sum_10': 1000,
    'limit_results_table': 20,
    'shift_count': 1,
    'shift_max_step': 1,
    'compare_group': False,
    'compare_len_limit': 0.0,
    'types_use_original': False,
    'types_compare_all': False,
    'cut_file_name_length_prefix': 10,
    'cut_file_name_length_suffix': 10,
    'limit_manual_distance': 1.0,
}

types_all = [
            "./AsString/Relative/Seconds/Post_Processed",
            # "./AsString/Absolute/Seconds/Post_Processed",
            ]

if f_params['types_use_original']:
    types_all.extend([
            # "./AsString/Relative/Seconds/Original",
            # "./AsString/Absolute/Seconds/Original",
            ])

distance_methods_all = [
    'manual_delta',
    'manual_count',
    'dtw',
    'area',
]

score_method_all = [
    'd_sum_10',
    'd_min',
    'count',
]


def compare_xml_all(a_video_small, a_video_big):
    fingerprints_small, streams_names_small, streams_count_small = get_fingerprints(a_video_small)
    fingerprints_big, streams_names_big, streams_count_big = get_fingerprints(a_video_big)

    for file_small in streams_names_small:
        start_time = datetime.datetime.now()

        print('{}) {} fingerprints: {}'.format(streams_names_small[file_small],
                                               len(fingerprints_small[streams_names_small[file_small]]['fingerprints']),
                                               file_small))

        fill_compare(fingerprints_small, streams_names_small, streams_count_small, fingerprints_big, streams_names_big,
                     streams_count_big, file_small)
        sort_compare(fingerprints_small, streams_names_small, streams_count_small, fingerprints_big, streams_names_big,
                     streams_count_big, file_small)
        calc_final(fingerprints_small, streams_names_small, streams_count_small, fingerprints_big, streams_names_big,
                   streams_count_big, file_small)
        calc_final_weighted(fingerprints_small, streams_names_small, streams_count_small, fingerprints_big,
                            streams_names_big, streams_count_big, file_small)

        print_table(fingerprints_small, streams_names_small, file_small)

        print('-------------------')
        stop_time = datetime.datetime.now()
        time_processed = stop_time - start_time
        print('finished: {} ({}..{})'.format(time_processed, start_time, stop_time))
        print('-------------------')

    print('end --------------------')


def get_fingerprints(a_video_dir):
    print('--------------------')

    if os.path.isabs(a_video_dir):
        video_dir = a_video_dir
    else:
        video_dir = os.path.join(os.getcwd() + '/' + a_video_dir)

    # detectors_all = alpha_detectors_all.get_all_detectors()
    finger_prints_all = alpha_detectors_all.get_all_finger_prints()

    fingerprints_from_dir = {}
    streams_names = {}
    streams_count = 0

    print('--------------------')
    print('scanning files...')

    for (dirpath, dirnames, filenames) in os.walk(video_dir):
        print('({} files) in {}'.format(len(filenames), dirpath))

        for file_name in filenames:
            if pathlib.Path(file_name).suffix in ['.xml']:

                full_path_video = os.path.join(dirpath, file_name)
                full_path_xml = os.path.join(dirpath, file_name)

                try:
                    tree = ET.ElementTree(file=full_path_xml)
                    root = tree.getroot()
                    for Item_Stream in root.findall('./Streams/Stream'):
                        streams_count += 1
                        steam = Item_Stream.get('index')
                        full_path_video_with_steam = full_path_video + '.' + steam

                        for Item_FileInfo in Item_Stream.findall('./Info/FileInfo'):
                            duration = float(Item_FileInfo.get('duration'))
                            avg_frame_rate = float(Item_FileInfo.get('avg_frame_rate'))

                        streams_names[full_path_video_with_steam] = streams_count
                        fingerprints_from_dir[streams_names[full_path_video_with_steam]] = {'compare': {}, 'fingerprints': [], 'full_path_video': full_path_video, 'duration': duration, 'avg_frame_rate': avg_frame_rate}

                        for Item_FingerPrintOne in Item_Stream.findall("./FingerPrintsAll/FingerPrintOne"):
                            name = Item_FingerPrintOne.get('name')
                            if name in finger_prints_all:
                                group = Item_FingerPrintOne.get('group')
                                for type in types_all:
                                    if type is not None:
                                        for Item_Type in Item_FingerPrintOne.findall(type):
                                            if (Item_Type.text is not None) and (Item_Type.text != ''):
                                                AsString = Item_Type.text
                                                AsList = [float(s) for s in AsString.split(',')]
                                                if len(AsList) >= 3:
                                                    fingerprints_from_dir[streams_names[full_path_video_with_steam]]['fingerprints'].append({'name': name, 'group': group, 'type': type, 'AsString': AsString, 'AsList': AsList})
                except Exception as E:
                    print('exception: {}: {}'.format(full_path_xml, str(E)))

    print('--------------------')
    print('total: {} xml files'.format(streams_count))

    print('--------------------')
    [print(param, ': ', str(f_params[param])) for param in f_params]
    print('--------------------')
    [print(str(finger_prints_all[finger_print])) for finger_print in finger_prints_all]
    print('--------------------')
    print(str(types_all))
    print('--------------------')

    return fingerprints_from_dir, streams_names, streams_count


def get_area(list_small, list_big):
    x_absolute = 0
    x_y_curve1 = []
    for value in list_small:
        x_absolute += value
        x_y_curve1.append((x_absolute, value))

    x_absolute = 0
    x_y_curve2 = []
    for value in list_big:
        x_absolute += value
        x_y_curve2.append((x_absolute, value))

    polygon_points = []  # creates a empty list where we will append the points to create the polygon
    for xyvalue in x_y_curve1:
        polygon_points.append([xyvalue[0], xyvalue[1]])  # append all xy points for curve 1
    for xyvalue in x_y_curve2[::-1]:
        polygon_points.append([xyvalue[0], xyvalue[1]])  # append all xy points for curve 2 in the reverse order (from last point to first point)
    for xyvalue in x_y_curve1[0:1]:
        polygon_points.append([xyvalue[0], xyvalue[1]])  # append the first point in curve 1 again, to it "closes" the polygon

    polygon = Polygon(polygon_points)
    area = polygon.area

    return area


def get_manual_delta(list_small, list_big):
    return get_manual_distance(list_small, list_big, False)

def get_manual_count(list_small, list_big):
    return get_manual_distance(list_small, list_big, True)

def get_manual_distance(list_small, list_big, use_count):
    list_small2 = []
    list_small2.append(list_big[0])
    for i in range(1, len(list_small)):
        list_small2.append(list_small2[i - 1] + list_small[i])

    list_big2 = []
    list_big2.append(list_big[0])
    for i in range(1, len(list_big)):
        list_big2.append(list_big2[i - 1] + list_big[i])

    distance = 0
    for i in range(len(list_small2)):
        min_distance = min(abs(np.array(list_big2[min(len(list_big2) - 1, max(i-10, 0)):i+10]) - list_small2[i]))
        if use_count:
            if min_distance > f_params['limit_manual_distance']:
                distance += 1
        else:
            distance += min_distance

    if use_count:
        distance2 = sum([1 for i in range(len(list_small2)) if min(abs(np.array(list_big2[min(len(list_big2) - 1, max(i-10, 0)):i+10]) - list_small2[i])) > f_params['limit_manual_distance']])
    else:
        distance2 = sum([min(abs(np.array(list_big2[min(len(list_big2) - 1, max(i - 10, 0)):i + 10]) - list_small2[i])) for i in range(len(list_small2))])
    assert(distance == distance2)

    return distance


def fill_compare(fingerprints_small, streams_names_small, streams_count_small, fingerprints_big, streams_names_big, streams_count_big, file_small):
    fingerprints_small[streams_names_small[file_small]]['compare'] = {}

    for file_big in streams_names_big:
        if streams_names_big[file_big] in fingerprints_big:
            if (fingerprints_small[streams_names_small[file_small]]['duration'] <= 2 * fingerprints_big[streams_names_big[file_big]]['duration']):
                fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]] = {'distances_sorted': None, 'distances_all': [], 'full_path_video': file_big}

                for fingerprint_small in fingerprints_small[streams_names_small[file_small]]['fingerprints']:
                    for fingerprint_big in fingerprints_big[streams_names_big[file_big]]['fingerprints']:
                        if (
                                (fingerprint_small['group'] == fingerprint_big['group']) and
                                ((f_params['compare_group']) or (fingerprint_small['name'] == fingerprint_big['name'])) and
                                ((f_params['types_compare_all']) or (fingerprint_small['type'] == fingerprint_big['type']))
                        ):
                            list_small = fingerprint_small['AsList'][1:]
                            list_big = fingerprint_big['AsList'][1:]

                            list_big_absolute = []
                            list_big_absolute.append(fingerprint_big['AsList'][0] + fingerprint_big['AsList'][1])
                            for i in range(1, len(fingerprint_big['AsList'][1:])):
                                list_big_absolute.append(list_big_absolute[i - 1] + fingerprint_big['AsList'][1:][i])

                            distances = {}

                            if 'manual_delta' in distance_methods_all:
                                distance_min = get_manual_delta(list_small, list_big)
                                distances['manual_delta'] = {'distance_min': distance_min, 'shifted_time_start': list_big_absolute[0], 'shifted_time_stop': list_big_absolute[-1]}

                            if 'manual_count' in distance_methods_all:
                                distance_min = get_manual_count(list_small, list_big)
                                distances['manual_count'] = {'distance_min': distance_min, 'shifted_time_start': list_big_absolute[0], 'shifted_time_stop': list_big_absolute[-1]}

                            if 'dtw' in distance_methods_all:
                                alignment = dtw(list_small, list_big, distance_only=True)
                                distance_min = alignment.distance
                                distances['dtw'] = {'distance_min': distance_min, 'shifted_time_start': list_big_absolute[0], 'shifted_time_stop': list_big_absolute[-1]}

                            if 'dtw' in distance_methods_all:
                                distance_min = get_area(list_small, list_big)
                                distances['area'] = {'distance_min': distance_min, 'shifted_time_start': list_big_absolute[0], 'shifted_time_stop': list_big_absolute[-1]}

                            if len(list_small) < len(list_big):
                                shift = min(int((len(list_big) - len(list_small)) / f_params['shift_count']), f_params['shift_max_step'])
                                if shift > 0:
                                    shifted_index = 0
                                    while (len(list_big) - shifted_index) > (1 - f_params['compare_len_limit']) * len(list_small):
                                        for shifted_len in range(int((1 - f_params['compare_len_limit']) * len(list_small)), 1 + int((1 + f_params['compare_len_limit']) * len(list_small))):
                                            if (shifted_index + shifted_len) < len(list_big):

                                                if 'dtw' in distance_methods_all:
                                                    alignment = dtw(list_small, list_big[shifted_index:shifted_index + shifted_len], distance_only=True)
                                                    distance_min = alignment.distance
                                                    if distances['dtw']['distance_min'] > distance_min:
                                                        distances['dtw']['distance_min'] = distance_min
                                                        distances['dtw']['shifted_time_start'] = list_big_absolute[shifted_index]
                                                        distances['dtw']['shifted_time_stop'] = list_big_absolute[shifted_index + shifted_len]

                                                if 'area' in distance_methods_all:
                                                    distance_min = get_area(list_small, list_big[shifted_index:shifted_index + shifted_len])
                                                    if distances['area']['distance_min'] > distance_min:
                                                        distances['area']['distance_min'] = distance_min
                                                        distances['area']['shifted_time_start'] = list_big_absolute[shifted_index]
                                                        distances['area']['shifted_time_stop'] = list_big_absolute[shifted_index + shifted_len]

                                                if 'manual_delta' in distance_methods_all:
                                                    distance_min = get_manual_delta(list_small, list_big[shifted_index:shifted_index + shifted_len])
                                                    if distances['manual_delta']['distance_min'] > distance_min:
                                                        distances['manual_delta']['distance_min'] = distance_min
                                                        distances['manual_delta']['shifted_time_start'] = list_big_absolute[shifted_index]
                                                        distances['manual_delta']['shifted_time_stop'] = list_big_absolute[shifted_index + shifted_len]

                                                if 'manual_count' in distance_methods_all:
                                                    distance_min = get_manual_count(list_small, list_big[shifted_index:shifted_index + shifted_len])
                                                    if distances['manual_count']['distance_min'] > distance_min:
                                                        distances['manual_count']['distance_min'] = distance_min
                                                        distances['manual_count']['shifted_time_start'] = list_big_absolute[shifted_index]
                                                        distances['manual_count']['shifted_time_stop'] = list_big_absolute[shifted_index + shifted_len]

                                        shifted_index += shift

                            fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_all'].append({
                                'distances': distances,
                                'name': fingerprint_small['name'],
                                'name_found': fingerprint_big['name'],
                                'group': fingerprint_small['group'],
                                'type': fingerprint_small['type']
                                })

                fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_sorted'] = {}
                fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_min'] = {}
                fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_sum_10'] = {}
                for distance_method in distance_methods_all:
                    fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_sorted'][distance_method] = sorted(
                        fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_all'],
                        key=lambda a_entry: a_entry['distances'][distance_method]['distance_min'])

                    if len(fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_sorted'][distance_method]) > 0:
                        fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_min'][distance_method] = fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_sorted'][distance_method][0]['distances'][distance_method]['distance_min']

                        if len(fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_sorted'][distance_method]) >= 10:
                            fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_sum_10'][distance_method] = sum(
                                [d['distances'][distance_method]['distance_min'] for d in fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_sorted'][distance_method][:10]]
                            )
                        else:
                            fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_sum_10'][distance_method] = (
                                sum([d['distances'][distance_method]['distance_min'] for d in fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_sorted'][distance_method]])
                                + fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_sorted'][distance_method][-1]['distances'][distance_method]['distance_min']
                                * (10 - len(fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_sorted'][distance_method]))
                                )
                    else:
                        fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_min'][distance_method] = None
                        fingerprints_small[streams_names_small[file_small]]['compare'][streams_names_big[file_big]]['distances_sum_10'][distance_method] = None

def sort_compare(fingerprints_small, streams_names_small, streams_count_small, fingerprints_big, streams_names_big,streams_count_big, file_small):
    fingerprints_small[streams_names_small[file_small]]['compare_sorted_min'] = {}
    fingerprints_small[streams_names_small[file_small]]['compare_sorted_sum_10'] = {}
    fingerprints_small[streams_names_small[file_small]]['compare_sorted_count'] = {}

    for file_big in fingerprints_small[streams_names_small[file_small]]['compare']:
        fingerprints_small[streams_names_small[file_small]]['compare'][file_big]['counts_all'] = {}

    for distance_method in distance_methods_all:
        compare_not_none = [fingerprints_small[streams_names_small[file_small]]['compare'][key]
                            for key in fingerprints_small[streams_names_small[file_small]]['compare']
                            if fingerprints_small[streams_names_small[file_small]]['compare'][key]['distances_min'].get(distance_method, None) is not None]
        fingerprints_small[streams_names_small[file_small]]['compare_sorted_min'][distance_method] = sorted(
            compare_not_none, key=lambda a_entry: a_entry['distances_min'][distance_method])

        compare_not_none = [fingerprints_small[streams_names_small[file_small]]['compare'][key]
                            for key in fingerprints_small[streams_names_small[file_small]]['compare']
                            if fingerprints_small[streams_names_small[file_small]]['compare'][key]['distances_sum_10'].get(distance_method, None) is not None]
        fingerprints_small[streams_names_small[file_small]]['compare_sorted_sum_10'][distance_method] = sorted(
            compare_not_none, key=lambda a_entry: a_entry['distances_sum_10'][distance_method])

        for file_big in fingerprints_small[streams_names_small[file_small]]['compare']:
            fingerprints_small[streams_names_small[file_small]]['compare'][file_big]['counts_all'][distance_method] = {'count': 0}

        finger_prints_all = alpha_detectors_all.get_all_finger_prints()
        for finger_print_name in finger_prints_all:
            for type in types_all:
                if type is not None:
                    distance_min = None
                    for file_big in fingerprints_small[streams_names_small[file_small]]['compare']:
                        for distance in fingerprints_small[streams_names_small[file_small]]['compare'][file_big]['distances_all']:
                            if (distance['name'] == finger_print_name) and (distance['type'] == type):
                                if distance_min is None:
                                    distance_min = distance['distances'][distance_method]['distance_min']
                                else:
                                    if distance_min > distance['distances'][distance_method]['distance_min']:
                                        distance_min = distance['distances'][distance_method]['distance_min']
                                break

                    if distance_min is not None:
                        for file_big in fingerprints_small[streams_names_small[file_small]]['compare']:
                            for distance in fingerprints_small[streams_names_small[file_small]]['compare'][file_big]['distances_all']:
                                if (distance['name'] == finger_print_name) and (distance['type'] == type):
                                    if distance_min == distance['distances'][distance_method]['distance_min']:
                                        fingerprints_small[streams_names_small[file_small]]['compare'][file_big]['counts_all'][distance_method]['count'] += 1
                                    break

        count_max = None
        for file_big in fingerprints_small[streams_names_small[file_small]]['compare']:
            if count_max is None:
                count_max = fingerprints_small[streams_names_small[file_small]]['compare'][file_big]['counts_all'][distance_method]['count']
            else:
                if count_max < fingerprints_small[streams_names_small[file_small]]['compare'][file_big]['counts_all'][distance_method]['count']:
                    count_max = fingerprints_small[streams_names_small[file_small]]['compare'][file_big]['counts_all'][distance_method]['count']

        if count_max is not None:
            for file_big in fingerprints_small[streams_names_small[file_small]]['compare']:
                fingerprints_small[streams_names_small[file_small]]['compare'][file_big]['counts_all'][distance_method]['is_max'] = (count_max == fingerprints_small[streams_names_small[file_small]]['compare'][file_big]['counts_all'][distance_method]['count'])
                fingerprints_small[streams_names_small[file_small]]['compare'][file_big]['counts_all'][distance_method]['count_max'] = count_max

        compare_not_none = [fingerprints_small[streams_names_small[file_small]]['compare'][key]
                            for key in fingerprints_small[streams_names_small[file_small]]['compare']
                            if fingerprints_small[streams_names_small[file_small]]['compare'][key]['counts_all'][distance_method]['count'] is not None]
        fingerprints_small[streams_names_small[file_small]]['compare_sorted_count'][distance_method] = sorted(
            compare_not_none,
            key=lambda a_entry: a_entry['counts_all'][distance_method]['count'],
            reverse=True)

def calc_final(fingerprints_small, streams_names_small, streams_count_small, fingerprints_big, streams_names_big, streams_count_big, file_small):
    fingerprints_small[streams_names_small[file_small]]['final_all'] = {}
    final = fingerprints_small[streams_names_small[file_small]]['final_all']

    for score_method in ['compare_sorted_sum_10', 'compare_sorted_min']:
        for distance_method in fingerprints_small[streams_names_small[file_small]][score_method]:
            for found_value in fingerprints_small[streams_names_small[file_small]][score_method][distance_method]:
                distance_min = found_value['distances_sorted'][distance_method][0]['distances'][distance_method]['distance_min']
                shifted_time_start = found_value['distances_sorted'][distance_method][0]['distances'][distance_method]['shifted_time_start']
                shifted_time_stop = found_value['distances_sorted'][distance_method][0]['distances'][distance_method]['shifted_time_stop']

                file_big = found_value['full_path_video']
                file_big_num = streams_names_big[file_big]

                if file_big_num not in final:
                    final[file_big_num] = {}

                if 'distances_all' not in final[file_big_num]:
                    final[file_big_num]['distances_all'] = {}

                if distance_method not in final[file_big_num]['distances_all']:
                    final[file_big_num]['distances_all'][distance_method] = {}

                if score_method not in final[file_big_num]['distances_all'][distance_method]:
                    final[file_big_num]['distances_all'][distance_method][score_method] = {}

                final[file_big_num]['file_big'] = file_big

                final[file_big_num]['distances_all'][distance_method][score_method]['distance_min'] = distance_min
                final[file_big_num]['distances_all'][distance_method][score_method]['shifted_time_start'] = shifted_time_start
                final[file_big_num]['distances_all'][distance_method][score_method]['shifted_time_stop'] = shifted_time_stop

    for file_big_num in final:
        shifted_time_start_sum_all = 0.0
        shifted_time_stop_sum_all = 0.0

        shifted_time_delta_min = None
        shifted_time_delta_min_value_start = None
        shifted_time_delta_min_value_stop = None

        for distance_method in final[file_big_num]['distances_all']:
            for score_method in final[file_big_num]['distances_all'][distance_method]:
                shifted_time_start_sum_1 = 0.0
                shifted_time_stop_sum_1 = 0.0
                for distance_method2 in final[file_big_num]['distances_all']:
                    for score_method2 in final[file_big_num]['distances_all'][distance_method2]:
                        if (distance_method != distance_method2) and (score_method != score_method2):
                            shifted_time_start_delta_1 = abs(
                                final[file_big_num]['distances_all'][distance_method][score_method]['shifted_time_start'] -
                                final[file_big_num]['distances_all'][distance_method2][score_method2]['shifted_time_start'])
                            shifted_time_stop_delta_1 = abs(
                                final[file_big_num]['distances_all'][distance_method][score_method]['shifted_time_stop'] -
                                final[file_big_num]['distances_all'][distance_method2][score_method2]['shifted_time_stop'])

                            shifted_time_start_sum_1 += shifted_time_start_delta_1
                            shifted_time_stop_sum_1 += shifted_time_stop_delta_1

                shifted_time_start_sum_all += shifted_time_start_sum_1
                shifted_time_stop_sum_all += shifted_time_stop_sum_1

                shifted_time_delta_1_sum = shifted_time_start_sum_1 + shifted_time_stop_sum_1

                if shifted_time_delta_min is None:
                    shifted_time_delta_min = shifted_time_delta_1_sum
                    shifted_time_delta_min_value_start = final[file_big_num]['distances_all'][distance_method][score_method]['shifted_time_start']
                    shifted_time_delta_min_value_stop = final[file_big_num]['distances_all'][distance_method][score_method]['shifted_time_stop']

                if shifted_time_delta_min > shifted_time_delta_1_sum:
                    shifted_time_delta_min = shifted_time_delta_1_sum
                    shifted_time_delta_min_value_start = final[file_big_num]['distances_all'][distance_method][score_method]['shifted_time_start']
                    shifted_time_delta_min_value_stop = final[file_big_num]['distances_all'][distance_method][score_method]['shifted_time_stop']

        if 'result' not in final[file_big_num]:
            final[file_big_num]['result'] = {}

        final[file_big_num]['result']['shifted_time_start_sum_all'] = shifted_time_start_sum_all
        final[file_big_num]['result']['shifted_time_stop_sum_all'] = shifted_time_stop_sum_all

        final[file_big_num]['result']['shifted_time_sum'] = shifted_time_start_sum_all + shifted_time_stop_sum_all

        final[file_big_num]['result']['shifted_time_delta_min'] = shifted_time_delta_min
        final[file_big_num]['result']['shifted_time_delta_min_value_start'] = shifted_time_delta_min_value_start
        final[file_big_num]['result']['shifted_time_delta_min_value_stop'] = shifted_time_delta_min_value_stop

    final_list = [{'key': file_big_num, 'value': final[file_big_num]} for file_big_num in final]
    fingerprints_small[streams_names_small[file_small]]['final_sorted_sum'] = sorted(final_list, key=lambda a_entry: a_entry['value']['result']['shifted_time_sum'])
    fingerprints_small[streams_names_small[file_small]]['final_sorted_min'] = sorted(final_list, key=lambda a_entry: a_entry['value']['result']['shifted_time_delta_min'])


def calc_final_weighted(fingerprints_small, streams_names_small, streams_count_small, fingerprints_big, streams_names_big, streams_count_big, file_small):
    fingerprints_small[streams_names_small[file_small]]['final_weighted'] = []
    final_weighted = fingerprints_small[streams_names_small[file_small]]['final_weighted']

    max_metric_count = None

    for file_big_num in fingerprints_small[streams_names_small[file_small]]['compare']:
        file_value = fingerprints_small[streams_names_small[file_small]]['compare'][file_big_num]

        file_distances_weighted_all = {'full_path_video': file_value['full_path_video'], 'distances_weighted_all': []}

        for metric_value in file_value['distances_all']:
            for distance_method in metric_value['distances']:
                distance_method_value = metric_value['distances'][distance_method]

                distance_weighted = {}
                distance_weighted['metric'] = metric_value['name']
                distance_weighted['distance_method'] = distance_method
                distance_weighted['distance_min'] = distance_method_value['distance_min']
                distance_weighted['shifted_time_start'] = distance_method_value['shifted_time_start']
                distance_weighted['shifted_time_stop'] = distance_method_value['shifted_time_stop']

                file_distances_weighted_all['distances_weighted_all'].append(distance_weighted)

        for metric_index in range(len(file_distances_weighted_all['distances_weighted_all'])):
            metric_value = file_distances_weighted_all['distances_weighted_all'][metric_index]
            sum_start = 0.0
            sum_stop = 0.0
            for metric_index2 in range(len(file_distances_weighted_all['distances_weighted_all'])):
                if metric_index != metric_index2:
                    metric_value2 = file_distances_weighted_all['distances_weighted_all'][metric_index2]

                    sum_start += abs(metric_value['shifted_time_start'] - metric_value2['shifted_time_start'])
                    sum_stop += abs(metric_value['shifted_time_stop'] - metric_value2['shifted_time_stop'])

            metric_value['shifted_time_difference'] = sum_start + sum_stop

        if max_metric_count is None:
            max_metric_count = len(file_distances_weighted_all['distances_weighted_all'])

        if max_metric_count < len(file_distances_weighted_all['distances_weighted_all']):
            max_metric_count = len(file_distances_weighted_all['distances_weighted_all'])

        sum_differences_weighted = 0.0
        for metric_index in range(len(file_distances_weighted_all['distances_weighted_all'])):
            metric_value = file_distances_weighted_all['distances_weighted_all'][metric_index]
            sum_differences_weighted += metric_value['shifted_time_difference'] * metric_value['distance_min']

        file_distances_weighted_all['sum_differences_weighted'] = sum_differences_weighted
        final_weighted.append(file_distances_weighted_all)

    for file_value in fingerprints_small[streams_names_small[file_small]]['final_weighted']:
        file_value['complete'] = 0 if (max_metric_count == 0) else len(file_value['distances_weighted_all']) / max_metric_count

    fingerprints_small[streams_names_small[file_small]]['final_weighted_sorted'] = sorted(final_weighted, key=lambda a_entry: a_entry['sum_differences_weighted'])


def cut_file_name(file_name):
    if file_name is None:
        return file_name

    if len(file_name) < (f_params['cut_file_name_length_prefix'] + f_params['cut_file_name_length_suffix'] + 3):
        return file_name

    return file_name[:f_params['cut_file_name_length_prefix']] + '...' + file_name[-f_params['cut_file_name_length_suffix']:]

def print_table(fingerprints_small, streams_names_small, file_small):
    # вывод таблицы
    table = []
    original_path, original_file = os.path.split(fingerprints_small[streams_names_small[file_small]]['full_path_video'])

    table_header_distance_method = [cut_file_name(original_file), '|', 'final', None, None, None, None, None, None, None, None, None, None, None, None, None]
    table_header_score_method = [None, '|', None, 'final_sum', None, None, '|', None, 'final_sum', None, None, '|', None, 'final_min', None, None]
    table_header = [None, '|', 'shift', '%', None, '', '|', 'shift', '%', None, '', '|', 'shift', '%', None, '']
    for distance_method in distance_methods_all:
        table_header_distance_method.extend(['|', distance_method, None, None, None, None, None, None, None, None, None, None, None, None, None])
        table_header_score_method.extend(['|', None, 'd_sum_10', None, None, '|', None, 'd_min', None, None, '|', None, 'count', None, None])
        table_header.extend(['|', 'shift', None, '%', 'd_sum_10', '|', 'shift', None, '%', 'd_min', '|', 'shift', None, '%', 'count'])
    table.append(table_header_distance_method)
    table.append(table_header_score_method)
    table.append(table_header)

    table_line = {}

    distance_method = 'final'
    table_line[distance_method] = {}

    score_method = 'final_weighted'
    table_line[distance_method][score_method] = []
    index_found = 0
    for found_value in fingerprints_small[streams_names_small[file_small]]['final_weighted_sorted']:
        if index_found >= f_params['limit_results_table']:
            break
        index_found += 1

        value = found_value['sum_differences_weighted']
        found_path, found_file = os.path.split(found_value['full_path_video'])
        complete = found_value['complete']

        table_line[distance_method][score_method].append({'value': value, 'found_file': found_file, 'complete': complete})

    score_method = 'final_sum'
    table_line[distance_method][score_method] = []
    index_found = 0
    for found_value in fingerprints_small[streams_names_small[file_small]]['final_sorted_sum']:
        if index_found >= f_params['limit_results_table']:
            break
        index_found += 1

        value = found_value['value']['result']['shifted_time_sum']
        found_path, found_file = os.path.split(found_value['value']['file_big'])

        table_line[distance_method][score_method].append({'value': value, 'found_file': found_file})

    score_method = 'final_min'
    table_line[distance_method][score_method] = []
    index_found = 0
    for found_value in fingerprints_small[streams_names_small[file_small]]['final_sorted_min']:
        if index_found >= f_params['limit_results_table']:
            break
        index_found += 1

        value = found_value['value']['result']['shifted_time_delta_min']
        found_path, found_file = os.path.split(found_value['value']['file_big'])
        shifted_time_start = found_value['value']['result']['shifted_time_delta_min_value_start']
        shifted_time_stop = found_value['value']['result']['shifted_time_delta_min_value_stop']

        table_line[distance_method][score_method].append({'value': value, 'found_file': found_file, 'shifted_time_start': shifted_time_start, 'shifted_time_stop': shifted_time_stop})

    for distance_method in distance_methods_all:
        table_line[distance_method] = {}

        table_line[distance_method]['table_sum_10'] = []
        index_found = 0
        for found_value in fingerprints_small[streams_names_small[file_small]]['compare_sorted_sum_10'][distance_method]:
            if index_found >= f_params['limit_results_table']:
                break
            index_found += 1

            value_sum_10 = found_value['distances_sum_10'][distance_method]
            found_path_sum_10, found_file_sum_10 = os.path.split(found_value['full_path_video'])
            percent_sum_10 = (f_params['limit_sum_10'] - value_sum_10) / f_params['limit_sum_10']
            shifted_time_start = found_value['distances_sorted'][distance_method][0]['distances'][distance_method]['shifted_time_start']
            shifted_time_stop = found_value['distances_sorted'][distance_method][0]['distances'][distance_method]['shifted_time_stop']

            table_line[distance_method]['table_sum_10'].append({'value': value_sum_10, 'found_file': found_file_sum_10, 'percent': percent_sum_10, 'shifted_time_start': shifted_time_start, 'shifted_time_stop': shifted_time_stop})

        table_line[distance_method]['table_min'] = []
        index_found = 0
        for found_value in fingerprints_small[streams_names_small[file_small]]['compare_sorted_min'][distance_method]:
            if index_found >= f_params['limit_results_table']:
                break
            index_found += 1

            value_min = found_value['distances_min'][distance_method]
            found_path_min, found_file_min = os.path.split(found_value['full_path_video'])
            percent_min = (f_params['limit_sum_10'] - value_min) / f_params['limit_sum_10']
            shifted_time_start = found_value['distances_sorted'][distance_method][0]['distances'][distance_method]['shifted_time_start']
            shifted_time_stop = found_value['distances_sorted'][distance_method][0]['distances'][distance_method]['shifted_time_stop']

            table_line[distance_method]['table_min'].append({'value': value_min, 'found_file': found_file_min, 'percent': percent_min, 'shifted_time_start': shifted_time_start, 'shifted_time_stop': shifted_time_stop})

        table_line[distance_method]['table_count'] = []
        index_found = 0
        for found_value in fingerprints_small[streams_names_small[file_small]]['compare_sorted_count'][distance_method]:
            if index_found >= f_params['limit_results_table']:
                break
            index_found += 1

            value_count = found_value['counts_all'][distance_method]['count']
            found_path_count, found_file_count = os.path.split(found_value['full_path_video'])
            percent_count = 0 if found_value['counts_all'][distance_method]['count_max'] == 0 else ((value_count) / found_value['counts_all'][distance_method]['count_max'])
            shifted_time_start = None
            shifted_time_stop = None

            table_line[distance_method]['table_count'].append({'value': value_count, 'found_file': found_file_count, 'percent': percent_count, 'shifted_time_start': shifted_time_start, 'shifted_time_stop': shifted_time_stop})

    max_len = 0 if (len(distance_methods_all) == 0) else max([len(table_line[distance_method][score_method]) for score_method in table_line[distance_method] for distance_method in distance_methods_all])

    for index_table in range(max_len):
        table_line_txt = [None]

        distance_method = 'final'

        score_method = 'final_weighted'
        if index_table < len(table_line[distance_method][score_method]):
            value = table_line[distance_method][score_method][index_table]['value']
            found_file = table_line[distance_method][score_method][index_table]['found_file']
            complete = table_line[distance_method][score_method][index_table]['complete']
        else:
            value = None
            found_file = None
            complete = None

        table_line_txt.extend(['|', None,
                               None if complete is None else '{:.0f}%'.format(complete * 100),
                               None if found_file is None else cut_file_name(found_file),
                               None if value is None else '{:.2f}'.format(value)
                               ])

        score_method = 'final_sum'
        if index_table < len(table_line[distance_method][score_method]):
            value = table_line[distance_method][score_method][index_table]['value']
            found_file = table_line[distance_method][score_method][index_table]['found_file']
        else:
            value = None
            found_file = None

        table_line_txt.extend(['|', None, None,
                               None if found_file is None else cut_file_name(found_file),
                               None if value is None else '{:.2f}'.format(value)])

        score_method = 'final_min'
        if index_table < len(table_line[distance_method][score_method]):
            value = table_line[distance_method][score_method][index_table]['value']
            found_file = table_line[distance_method][score_method][index_table]['found_file']
            # percent = int(100 * table_line[distance_method][score_method][index_table]['percent'])
            shifted_time_start = table_line[distance_method][score_method][index_table]['shifted_time_start']
            shifted_time_stop = table_line[distance_method][score_method][index_table]['shifted_time_stop']
        else:
            value = None
            found_file = None
            # percent = None
            shifted_time_start = None
            shifted_time_stop = None

        table_line_txt.extend(['|', None if (shifted_time_start is None) or (shifted_time_stop is None) else '{:.0f}..{:.0f}'.format(shifted_time_start, shifted_time_stop),
                               None,
                               None if found_file is None else cut_file_name(found_file),
                               None if value is None else '{:.2f}'.format(value)])

        for distance_method in distance_methods_all:
            for score_method in table_line[distance_method]:
                if index_table < len(table_line[distance_method][score_method]):
                    value = table_line[distance_method][score_method][index_table]['value']
                    found_file = table_line[distance_method][score_method][index_table]['found_file']
                    percent = int(100*table_line[distance_method][score_method][index_table]['percent'])
                    shifted_time_start = table_line[distance_method][score_method][index_table]['shifted_time_start']
                    shifted_time_stop = table_line[distance_method][score_method][index_table]['shifted_time_stop']
                else:
                    value = None
                    found_file = None
                    percent = None
                    shifted_time_start = None
                    shifted_time_stop = None

                table_line_txt.extend(['|', None if (shifted_time_start is None) or (shifted_time_stop is None) else '{:.0f}..{:.0f}'.format(shifted_time_start, shifted_time_stop), None if found_file is None else cut_file_name(found_file), percent, None if value is None else '{:.2f}'.format(value)])

        table.append(table_line_txt)

    print(tabulate(table))



# trapz
# import numpy as np
# from scipy.integrate import simps
# from numpy import trapz
# x = np.linspace(0, 5, 21)
# y = np.pi / np.exp(x)
# # dx - растояние между соседними X координатами
# area = trapz(y, dx=5/20)
# Результат:
# In [19]: simps(y, dx=5/20)
# Out[19]: 3.1204919857832971
# In [20]: trapz(y, dx=5/20)
# Out[20]: 3.1366600769000623




# 2. Contour Area
# Contour area is given by the function cv.contourArea() or from moments, M['m00'].
# area = cv.contourArea(cnt)

