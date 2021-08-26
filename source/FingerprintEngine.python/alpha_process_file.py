import alpha_show_graphics
import alpha_xml
from Detectors.Lists import alpha_detectors_all

import ffmpeg

import numpy as np
import datetime
import os
import sys
import traceback

def process_file(file_name, mode=None, a_frame_index=0, need_detectors=None):
    video_file = {'video_file': file_name}

    probe = ffmpeg.probe(video_file['video_file'])

    video_streams_all = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']

    for video_stream_index in range(len(video_streams_all)):
        video_stream = video_streams_all[video_stream_index]

        video_file['width'] = int(video_stream['width'])
        video_file['height'] = int(video_stream['height'])
        video_file['duration'] = float(video_stream['duration'])

        avg_frame_rate = video_stream['avg_frame_rate'].split('/')
        if int(avg_frame_rate[1]) != 0:
            video_file['avg_frame_rate'] = float(int(avg_frame_rate[0]) / int(avg_frame_rate[1]))
        else:
            avg_frame_rate = video_stream['r_frame_rate'].split('/')
            if int(avg_frame_rate[1]) != 0:
                video_file['avg_frame_rate'] = float(int(avg_frame_rate[0]) / int(avg_frame_rate[1]))
            else:
                video_file['avg_frame_rate'] = None

        video_file['frames_by_fps'] = int(video_file['duration'] * video_file['avg_frame_rate'])
        video_file['frames_actual'] = -1

        if mode == 'show_time_line_one':
            # график выбранной метрики по всем значениям
            time_line_all = np.empty((0), {})

        if (mode == 'process_file') or (mode == 'process_dir'):
            detectors_all = alpha_detectors_all.get_all_detectors()
            if (need_detectors is None) or (need_detectors == []):
                detectors = detectors_all
            else:
                detectors = {}
                for d in need_detectors:
                    detectors[d] = detectors_all[d]

            print('---------------')
            for index, (key, value) in enumerate(detectors.items()):
                print('detector {:04d}/{:d}: {}'.format(index, len(detectors), key))
            print('---------------')

            # XML для результатов
            file_name_xml, Root_Tree, Item_Progress_Stream = alpha_xml.create_xml(video_file, video_stream_index, detectors)
            Root_Tree.write(file_name_xml, encoding="utf-8")

            # статистика по времени обработки
            start_time = datetime.datetime.now()
            stop_time = -1
            time_processed = -1
            Item_Progress_Stream.set('start_time', str(start_time.strftime(alpha_xml.__DATE_TIME_FORMAT)))

            for detector_key in detectors:
                detectors[detector_key]['detector'].process_init(video_file, detectors[detector_key]['xml_item'])
                detectors[detector_key]['last'] = [None]

        print('-------------------')
        print('file:', video_file['video_file'])
        print('-------------------')
        print('{} ({} seconds); {} frames; framesize={}*{}'.format(
            datetime.timedelta(seconds=int(video_file['duration'])), int(video_file['duration']),
            video_file['frames_by_fps'],
            video_file['width'], video_file['height'],
        ))
        print('-------------------')

        frame_index = 0

        try:
            # грузим видео в память
            part_path, part_name = os.path.split(video_file['video_file'])
            file_name_raw = '__temp_raw_(' + part_name + ').raw'
            if os.path.exists(file_name_raw):
                os.remove(file_name_raw)

            out, _ = (ffmpeg.input(video_file['video_file'])
                      # .trim(start_frame=0, end_frame=10)
                      # .output('pipe:', format='rawvideo', pix_fmt='rgb24') # RGB
                      # .output('pipe:', format='rawvideo', pix_fmt='yuv420p')  # YUV
                      .output(file_name_raw, format='rawvideo', pix_fmt='yuv420p', map="0:v:"+str(video_stream_index))  # YUV
                      .global_args('-loglevel', 'panic', '-stats')
                      # .run(capture_stdout=True)
                      .run()
                      )

            print('---------------')

            detectors_exception = []
            frame_size_yuv = int(video_file['height'] * video_file['width'] * 3 / 2)

            test_save_all = False
            if test_save_all:
                test_back = False
                test_frames_all = []


            with open(file_name_raw, 'rb') as file_raw:
                while True:
                    batch = file_raw.read(frame_size_yuv)
                    if not test_save_all:
                        if (batch is None) or (batch == b''):
                            break;
                    video = (np.frombuffer(batch, np.uint8)
                         # .reshape([-1, height, width, 3]) # RGB
                         .reshape([-1, frame_size_yuv])  # YUV
                         )

                    for image in video[:]:
                        if test_save_all:
                            test_frames_all.append({'image': image})
                        if (mode == 'process_file') or (mode == 'process_dir'):
                            for detector_key in detectors:
                                if detector_key not in detectors_exception:
                                    try:
                                        if test_save_all:
                                            image_for_process = test_frames_all[frame_index]['image']
                                            last_value_for_process = None if (frame_index == 0) else test_frames_all[frame_index - 1]['result']['value_for_save']
                                        else:
                                            image_for_process = image
                                            last_value_for_process = detectors[detector_key]['last'][0]

                                        result = detectors[detector_key]['detector'].process_frame(
                                            frame_index, image_for_process,
                                            video_file['height'],
                                            video_file['width'],
                                            detectors[detector_key]['xml_item'],
                                            last_value_for_process
                                            )
                                        value, change, detectors[detector_key]['last'][0] = result['value'], result['change'], result['value_for_save']

                                        if test_save_all:
                                            test_frames_all[frame_index]['result'] = result

                                    except Exception as E:
                                        print('exception: {}: {}'.format(detector_key, str(E)))
                                        traceback.print_exc(file=sys.stdout)
                                        detectors_exception.append(detector_key)

                                if (mode == 'show_time_line_one') and (detector_key == a_detector_key):
                                    time_line_all = np.append(time_line_all, {'value': value, 'change': change})

                            show_statistic = True
                            if (frame_index >= 10):   show_statistic = ((frame_index % 10) == 0)
                            if (frame_index >= 100):  show_statistic = ((frame_index % 100) == 0)
                            # if (frame_index >= 1000): show_statistic = ((frame_index % 1000) == 0)

                            if show_statistic:
                                sys.stdout.write('\rframe {:5d} / {:d}'.format(frame_index, video_file['frames_by_fps']))
                                sys.stdout.flush()

                                Item_Progress_Stream.set('frames_processed', str(frame_index))
                                Item_Progress_Stream.set('finished', str(False))
                                Root_Tree.write(file_name_xml, encoding="utf-8")

                        if (mode == 'show_frame') and (frame_index == a_frame_index):
                            # test - показать один кадр на экране
                            alpha_show_graphics.show_image_pylab(image, video_file['height'], video_file['width'])
                            exit()

                        if test_save_all and test_back:
                            frame_index -= 1
                        else:
                            frame_index += 1
        finally:
            os.remove(file_name_raw)

        if (mode == 'process_file') or (mode == 'process_dir'):
            video_file['frames_actual'] = frame_index
            for Item_FileInfo in Root_Tree.findall("./Info/FileInfo"):
                Item_FileInfo.set('frames_actual', str(video_file['frames_actual']))
            Root_Tree.write(file_name_xml, encoding="utf-8")

            for detector_key in detectors:
                detectors[detector_key]['detector'].post_process(video_file, detectors[detector_key]['xml_item'])
                for finger_print_name in detectors[detector_key]['xml_item']:
                    Item_Progress_Detector = detectors[detector_key]['xml_item'][finger_print_name].findall("./Progress_FingerPrint")[0]
                    Item_Progress_Detector.set('finished', str(True))

            # завершаем статистику в XML
            Item_Progress_Stream.set('finished', str(True))
            Item_Progress_Stream.set('frames_processed', str(frame_index))
            stop_time = datetime.datetime.now()
            Item_Progress_Stream.set('stop_time', str(stop_time.strftime(alpha_xml.__DATE_TIME_FORMAT)))
            time_processed = stop_time - start_time
            Item_Progress_Stream.set('time_processed', str(time_processed))
            Root_Tree.write(file_name_xml, encoding="utf-8")

            print()
            print('frame {:5d} / {:d}'.format(frame_index, video_file['frames_actual']))
            print('-------------------')
            print('finished: {} ({}..{})'.format(time_processed, start_time, stop_time))
            print('-------------------')

        if mode == 'show_time_line_one':
            # график выбранной метрики по всем значениям
            alpha_show_graphics.show_time_line(time_line_all, video_file['duration'])

        if mode == 'show_time_line_all':
            # график всех метрик только что обработанного файла
            alpha_xml.show_xml_details(video_file['video_file'] + '.xml')

