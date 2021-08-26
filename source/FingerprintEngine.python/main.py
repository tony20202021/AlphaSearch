#coding: utf-8

# further reading:
# Fritz AI Python Library - https://pypi.org/project/fritz/
# cv2 https://docs.opencv.org/3.4/d2/d96/tutorial_py_table_of_contents_imgproc.html
# repository\visualrecognition\info\cv_dl_resource_guide.pdf
# https://www.google.com/search?q=opencv+python&oq=opencv&aqs=chrome.1.69i57j69i59j0l3j69i60l3.3206j0j4&sourceid=chrome&ie=UTF-8
# https://www.pyimagesearch.com/2016/06/20/detecting-cats-in-images-with-opencv/
# https://habr.com/ru/post/312714/
# https://habr.com/ru/company/jetinfosystems/blog/518264/
# https://habr.com/ru/company/jetinfosystems/blog/523272/
# https://habr.com/ru/company/intel/blog/519092/
# https://habr.com/ru/company/intel/blog/254747/
# https://github.com/openvinotoolkit
# https://habr.com/ru/post/436744/
# https://pypi.org/project/dlib/
# https://azure.microsoft.com/en-us/free/cognitive-services/
# https://habr.com/ru/company/intel/blog/254747/
# https://github.com/qrzeller/OpenCV-Video-Comparison
# https://russia-students.ru/materials/cv-academy

import alpha_process_dir
import alpha_process_file
import alpha_xml
import alpha_compare_xml

import argparse

modes_all = [
    'process_dir',
    'process_file',
    'show_xml_details',
    'show_xml_summary',
    'show_xml_compare',
    'show_frame',
    'show_time_line_one',
    'show_time_line_all',
    'compare_xml_all',
    'xml_version_update',
    'clear_locks',
    ]

# ffmpeg -ss 00:00:00 -i "01-Disney's-HELLO .avi" -to 00:02:00 -c copy num002.mp4
# -d "f:\My Downloads3"

# -m process_file -f "../../../../data/big/На работу в понедельник.wmv"
# -m process_file -f "../../../../data/small/На работу в понедельник.wmv_smartphone_t_video5393233829936761155.mp4"
# -m process_file -f "../../../../data/small/На работу в понедельник.wmv_smartphone_VID_20201216_210917.mp4"

# -m process_file -f "../../../../data/big/3/01-Disney's-HELLO .avi"
# -m process_file -f "../../../../data/big/3/01-Disney's-HELLO .avi_trim_3_40_1_30_num002.avi"
# -m process_file -f "../../../../data/small/3/01-Disney's-HELLO .avi_smartphone_VID_20201223_194450.mp4"

# -m process_file -f "../../../../data/big/hands/HANDSS.AVI"
# -m process_file -f "../../../../data/small/hands/HANDSS.AVI_smartphone_VID_20201223_193635.mp4"

# -m process_file -f "../../../../data/big/03= Кости =1-й Чемпионат Мира.mpg"
# -m process_file -f "../../../../data/03= Кости =1-й Чемпионат Мира.mpg_smartphone_VID_20201223_193744.mp4"
# -m process_file -f "f:\My Downloads3\video\02= Интересно и Удивительно\03= Кости =1-й Чемпионат Мира.mpg"

# -m process_file -f "../../../../data/big/cats/extremecats.wmv"


# -m process_dir -d "../../../../data/big/3"
# -m process_dir -d "../../../../data/small/3"

# -m show_frame -f "../../../../data/3/01-Disney's-HELLO .avi" -fi 170

# -m show_xml_details -f "../../../../data/big/3/01-Disney's-HELLO .avi"
# -m show_xml_details -f "../../../../data/big/3/01-Disney's-HELLO .avi_trim_3_40_1_30_num002.avi"
# -m show_xml_details -f "../../../../data/small/3/01-Disney's-HELLO .avi_smartphone_VID_20201223_194450.mp4"
# -m show_xml_details -f "../../../../data/big/На работу в понедельник.wmv"

# -m show_xml_summary -fk Change_Luma_0_05 -f "../../../../data/big/extremecats.wmv"
# -m show_xml_summary -fk Change_Luma_0_05 -f "../../../../data/big/3/01-Disney's-HELLO .avi"
# -m show_xml_summary -fk Change_Luma_0_05 -f "../../../../data/big/3/01-Disney's-HELLO .avi_trim_3_40_1_30_num002.avi"
# -m show_xml_summary -fk Change_Luma_0_05 -f "../../../../data/small/3/01-Disney's-HELLO .avi_smartphone_VID_20201223_194450.mp4"

# -m show_xml_compare -fk Change_Luma_0_05 -f1 "../../../../data/small/3/smartphone/01-Disney's-HELLO .avi_smartphone_VID_20201223_194450.mp4" -f2 "../../../../data/big/3/trim/avi/01-Disney's-HELLO .avi_trim_3_40_1_30_num002.avi" -fs1 +109
# -m show_xml_compare -fk Change_Luma_0_05 -f1 "../../../../data/small/3/smartphone/01-Disney's-HELLO .avi_smartphone_VID_20201223_194450.mp4" -f2 "../../../../data/big/3/trim/mp4/01-Disney's-HELLO .avi_trim_3_40_1_30_num002.mp4.xml" -fs1 +109
# -m show_xml_compare -fk Change_Luma_0_05 -f1 "../../../../data/small/3/smartphone/01-Disney's-HELLO .avi_smartphone_VID_20201223_194450.mp4" -f2 "../../../../data/big/3/all/01-Disney's-HELLO .avi" -fs1 +6670

# -m show_xml_compare -fk Change_Luma_0_05 -f1 "../../../../data/big/3/trim/avi/01-Disney's-HELLO .avi_trim_3_40_1_30_num002.avi" -f2 "../../../../data/big/3/all/01-Disney's-HELLO .avi" -fs1 +5500
# -m show_xml_compare -fk Change_Luma_0_05 -f1 "../../../../data/big/3/trim/avi/01-Disney's-HELLO .avi_trim_3_40_1_30_num002.avi.xml" -f2 "../../../../data/big/3/trim/mp4/01-Disney's-HELLO .avi_trim_3_40_1_30_num002.mp4.xml" -fs1 +0

# -m show_xml_compare -fk Change_Luma_0_05 -f1 "../../../../data/big/3/trim/mp4/01-Disney's-HELLO .avi_trim_3_40_1_30_num002.mp4.xml" -f2 "../../../../data/big/3/all/01-Disney's-HELLO .avi" -fs1 +5500

# -m show_xml_compare -fk Change_Luma_0_05 -f1 "../../../../data/small/hands/HANDSS.AVI_smartphone_VID_20201223_193635.mp4" -f2 "../../../../data/big/hands/HANDSS.AVI"
# -m show_xml_compare -fk Change_Luma_0_05 -f1 "../../../../data/small/hands/HANDSS.AVI_smartphone_VID_20201223_193635.mp4" -f2 "../../../../data/big/monday/На работу в понедельник.wmv"
# -m show_xml_compare -fk Change_Luma_0_05 -f1 "../../../../data/small/hands/HANDSS.AVI_smartphone_VID_20201223_193635.mp4" -f2 "../../../../data/big/cats/extremecats.wmv" -fs1 +32

# -m show_xml_compare -fk Change_Luma_0_05 -f1 "../../../../data/small/2/Баюшки-Баю (мф-Бременские Музыканты-2).mpg_smartphone_VID_20201223_193431.mp4" -f2 "../../../../data/big/2/Баюшки-Баю (мф-Бременские Музыканты-2).mpg"


# -m show_xml_details -fk Change_Luma_0_2 -f "../../../../data/small/3/01-Disney's-HELLO .avi_smartphone_VID_20201223_194450.mp4"
# -m show_xml_details -fk Change_Luma_0_2 -f "../../../../data/big/3/01-Disney's-HELLO .avi"

# -m compare_xml_all -ds "../../../../data/small/3" -db "../../../../data/big"
# -m compare_xml_all -ds "../../../../data/big/3/trim/avi" -db "../../../../data/big/3/all"
# -m compare_xml_all -ds "../../../../data/small/hands" -db "../../../../data/big/hands"
# -m compare_xml_all -ds "../../../../data/small/hands" -db "../../../../data/big"
# -m compare_xml_all -ds "../../../../data/small" -db f:\
# -m compare_xml_all -ds "../../../../data/big/4" -db "f:\My Downloads2\фильмы"

parser = argparse.ArgumentParser(description='Alpha Video search')
parser.add_argument('-m', '-mode', action="store", type=str, dest="mode", default='process_dir', choices=modes_all)
parser.add_argument('-d', '-dir', action="store", type=str, dest="dir",  default='../../../../data')
parser.add_argument('-ds', '-dir_small', action="store", type=str, dest="dir_small",  default='../../../../data/small')
parser.add_argument('-db', '-dir_big', action="store", type=str, dest="dir_big",  default='../../../../data/big')
parser.add_argument('-e', '-ext', action="store", type=str, dest="ext",  default="avi,mpg,wmv,mp4")
parser.add_argument('-f', '-file', action="store", type=str, dest="file")
parser.add_argument('-f1', '-file_1', action="store", type=str, dest="file_1")
parser.add_argument('-f2', '-file_2', action="store", type=str, dest="file_2")
parser.add_argument('-fs1', '-file_shift_1', action="store", type=int, dest="file_shift_1")
parser.add_argument('-fi', '-frame_index', action="store", type=int, dest="frame_index",  default=0)
parser.add_argument('-dk', '-detector_key', action="store", type=str, dest="detector_key",  default=None)
parser.add_argument('-fk', '-fingerprint_key', action="store", type=str, dest="fingerprint_key",  default=None)
args = parser.parse_args()

print('---------------')
print('mode: {}'.format(args.mode))
print('dir: {}'.format(args.dir))
print('dir_small: {}'.format(args.dir_small))
print('dir_big: {}'.format(args.dir_big))
print('ext: {}'.format(args.ext))
print('file: {}'.format(args.file))
print('file_1: {}'.format(args.file_1))
print('file_2: {}'.format(args.file_2))
print('file_shift_2: {}'.format(args.file_shift_1))
print('frame_index: {}'.format(args.frame_index))
print('detector_key: {}'.format(args.detector_key))
print('fingerprint_key: {}'.format(args.fingerprint_key))
print('---------------')

if args.mode == 'process_dir':
    alpha_process_dir.process_dir(args.dir, args.ext)

elif args.mode == 'process_file':
    alpha_process_file.process_file(args.file, mode=args.mode)

elif args.mode == 'show_xml_details':
    # показать готовые графики - по метрике
    alpha_xml.show_xml_details(args.file, args.fingerprint_key)

elif args.mode == 'show_xml_summary':
    # показать готовые графики - по метрике
    alpha_xml.show_xml_summary(args.file, args.fingerprint_key)

elif args.mode == 'show_xml_compare':
    # показать графики 2 файлов - по 1 метрике
    alpha_xml.show_xml_compare(args.file_1, args.file_2, args.fingerprint_key, args.file_shift_1)

elif args.mode == 'show_frame':
    alpha_process_file.process_file(args.file, mode=args.mode, a_frame_index=args.frame_index)

elif args.mode == 'show_time_line_one':
    alpha_process_file.process_file(args.file, mode=args.mode, a_detector_key=args.detector_key)

elif args.mode == 'show_time_line_all':
    alpha_process_file.process_file(args.file, mode=args.mode)

elif args.mode == 'compare_xml_all':
    alpha_compare_xml.compare_xml_all(args.dir_small, args.dir_big)

elif args.mode == 'xml_version_update':
    alpha_xml.xml_version_update(args.dir)

elif args.mode == 'clear_locks':
    alpha_process_dir.clear_locks(args.dir)


