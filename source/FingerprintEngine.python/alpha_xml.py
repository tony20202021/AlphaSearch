import xml.etree.ElementTree as ET
import datetime
import alpha_show_graphics
import alpha_compare_xml
from shapely.geometry import Polygon

from Detectors.Lists import alpha_detectors_all
import os
import pathlib

__FORMAT_VERSION = '02.03'
__DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
__XML_ID_TAG_NAME = 'AlphaSearchId'
__XML_ID_TAG_VALUE = '{C2E1FD9D-384D-46CE-A4F4-47FB295EF326}'

def find_or_create_item(root_item, parent_item, parent_path, item_name):
    if len(root_item.findall(parent_path + "/" + item_name)) > 0:
        item = root_item.findall(parent_path + "/" + item_name)[0]
    else:
        item = ET.SubElement(parent_item, item_name)
    return item


def create_xml(video, video_stream_index, detectors):
    file_name_xml = video['video_file'] + '.xml'

    if os.path.exists(file_name_xml):
        Root_Tree = ET.ElementTree(file=file_name_xml)
        Root_Data = Root_Tree.findall(".")[0]
    else:
        Root_Data = ET.Element('Data')
        Root_Tree = ET.ElementTree(Root_Data)

    Root_Data.set(__XML_ID_TAG_NAME, __XML_ID_TAG_VALUE)

    Item_Format = find_or_create_item(Root_Tree, Root_Data, ".", "Format")
    Item_Format.set('format_version', __FORMAT_VERSION)

    Item_Streams = find_or_create_item(Root_Tree, Root_Data, ".", "Streams")
    Item_VideoStream = find_or_create_item(Item_Streams, Item_Streams, ".", "Stream")
    Item_VideoStream.set("index", str(video_stream_index))

    Item_Info = find_or_create_item(Item_VideoStream, Item_VideoStream, ".", "Info")

    Item_FileName = find_or_create_item(Item_Info, Item_Info, ".", "FileName")
    Item_FileName.set('name', 'FileName')
    Item_FileName.text = video['video_file']

    Item_FileInfo = find_or_create_item(Item_Info, Item_Info, ".", "FileInfo")
    Item_FileInfo.set('duration', str(video['duration']))
    Item_FileInfo.set('bytes', '0')
    Item_FileInfo.set('avg_frame_rate', str(video['avg_frame_rate']))
    Item_FileInfo.set('frames_by_fps', str(video['frames_by_fps']))
    Item_FileInfo.set('frames_by_fps', str(video['frames_by_fps']))
    Item_FileInfo.set('frames_actual', str(video['frames_actual']))

    Item_FrameSize = find_or_create_item(Item_FileInfo, Item_FileInfo, ".", "FrameSize")
    Item_FrameSize.set('width', str(video['width']))
    Item_FrameSize.set('height', str(video['height']))

    Item_Progress_Stream = find_or_create_item(Item_VideoStream, Item_VideoStream, ".", "Progress_Stream")
    Item_Progress_Stream.set('frames_processed', str(0))

    Item_FingerPrintsAll = find_or_create_item(Item_VideoStream, Item_VideoStream, ".", "FingerPrintsAll")

    for detector_key in detectors:
        detectors[detector_key]['xml_item'] = {}

        for finger_print in detectors[detector_key]['detector'].get_finger_prints():
            for Item_FingerPrintOne in Item_FingerPrintsAll.findall("./FingerPrintOne"):
                if Item_FingerPrintOne.get('name') == finger_print['finger_print_name']:
                    Item_FingerPrintsAll.remove(Item_FingerPrintOne)
                    break

            detectors[detector_key]['xml_item'][finger_print['finger_print_name']] = ET.SubElement(Item_FingerPrintsAll, 'FingerPrintOne')

            detectors[detector_key]['xml_item'][finger_print['finger_print_name']].set('name', finger_print['finger_print_name'])
            detectors[detector_key]['xml_item'][finger_print['finger_print_name']].set('group', finger_print['group'])
            detectors[detector_key]['xml_item'][finger_print['finger_print_name']].set('detector', finger_print['detector'])
            detectors[detector_key]['xml_item'][finger_print['finger_print_name']].set('detector_id', str(detectors[detector_key]['detector'].f_id))
            detectors[detector_key]['xml_item'][finger_print['finger_print_name']].set('detector_version', str(detectors[detector_key]['detector'].f_version))
            detectors[detector_key]['xml_item'][finger_print['finger_print_name']].set('detector_params', str(detectors[detector_key]['detector'].f_params))

            Item_Progress_FingerPrint = find_or_create_item(detectors[detector_key]['xml_item'][finger_print['finger_print_name']], detectors[detector_key]['xml_item'][finger_print['finger_print_name']], ".", "Progress_FingerPrint")
            Item_Progress_FingerPrint.set('finished', str(False))

            Item_AsString = find_or_create_item(detectors[detector_key]['xml_item'][finger_print['finger_print_name']], detectors[detector_key]['xml_item'][finger_print['finger_print_name']], ".", "AsString")

            # AsString - Relative/Absolute, Seconds/Frames, Original/Post_Processed
            Item_Relative = find_or_create_item(Item_AsString, Item_AsString, ".", "Relative")
            Item_Seconds = find_or_create_item(Item_Relative, Item_Relative, ".", "Seconds")
            Item_Original = find_or_create_item(Item_Seconds, Item_Seconds, ".", "Original")
            Post_Processed = find_or_create_item(Item_Seconds, Item_Seconds, ".", "Post_Processed")
            Item_Frames = find_or_create_item(Item_Relative, Item_Relative, ".", "Frames")
            Item_Original = find_or_create_item(Item_Frames, Item_Frames, ".", "Original")
            Post_Processed = find_or_create_item(Item_Frames, Item_Frames, ".", "Post_Processed")
            Item_Absolute = find_or_create_item(Item_AsString, Item_AsString, ".", "Absolute")
            Item_Seconds = find_or_create_item(Item_Absolute, Item_Absolute, ".", "Seconds")
            Item_Original = find_or_create_item(Item_Seconds, Item_Seconds, ".", "Original")
            Post_Processed = find_or_create_item(Item_Seconds, Item_Seconds, ".", "Post_Processed")
            Item_Frames = find_or_create_item(Item_Absolute, Item_Absolute, ".", "Frames")
            Item_Original = find_or_create_item(Item_Frames, Item_Frames, ".", "Original")
            Post_Processed = find_or_create_item(Item_Frames, Item_Frames, ".", "Post_Processed")

            Item_Details = find_or_create_item(detectors[detector_key]['xml_item'][finger_print['finger_print_name']], detectors[detector_key]['xml_item'][finger_print['finger_print_name']], ".", "Details")

    return file_name_xml, Root_Tree, Item_Progress_Stream

def show_xml_details(file_name, a_fingerprint_name = None, a_type = None):
    duration = None
    time_lines_all = []

    if pathlib.Path(file_name).suffix.lower() != '.xml':
        file_name += '.xml'

    tree = ET.ElementTree(file=file_name)
    root = tree.getroot()
    for Item_Data in root.iter('Data'):
        for Item_Info in Item_Data.iter('Info'):
            for Item_FileInfo in Item_Info.iter('FileInfo'):
                duration = Item_FileInfo.get('duration')
                frames = Item_FileInfo.get('frames_by_fps')
        for Item_FingerPrintsAll in root.iter('FingerPrintsAll'):
            for Item_FingerPrintOne in Item_FingerPrintsAll.iter('FingerPrintOne'):
                fingerprint_name = Item_FingerPrintOne.get('name')
                if (a_fingerprint_name is None) or (fingerprint_name in a_fingerprint_name):
                    if a_type is None:
                        for Item_Details in Item_FingerPrintOne.iter('Details'):
                            plot = []
                            for Item_Change in Item_FingerPrintOne.iter('Change'):
                                plot.append({
                                    'x': int(Item_Change.get('frame_index')),
                                    # 'value': float(Item_Change.get('value')),
                                    'y': float(Item_Change.get('change')),
                                })
                    time_lines_all.append({'name': fingerprint_name, 'values': plot, 'duration': float(duration), 'frames': int(frames)})

    alpha_show_graphics.show_time_line(time_lines_all, file_name)


def get_time_line(time_lines_all, file_name, a_fingerprint_name, types_summary, a_subplot_name=None, a_plot_label=None, a_file_shift_frames=0, a_skip_values=0):
    if pathlib.Path(file_name).suffix.lower() != '.xml':
        file_name += '.xml'

    tree = ET.ElementTree(file=file_name)
    root = tree.getroot()

    for Item_Stream in root.findall('./Streams/Stream'):
        for Item_FileInfo in Item_Stream.findall('./Info/FileInfo'):
            duration = Item_FileInfo.get('duration')
            frames = Item_FileInfo.get('frames_by_fps')

    for Item_FingerPrintOne in Item_Stream.findall('./FingerPrintsAll/FingerPrintOne'):
        fingerprint_name = Item_FingerPrintOne.get('name')
        if (a_fingerprint_name is None) or (fingerprint_name in a_fingerprint_name):
            for type in types_summary:
                for Item_Type in Item_FingerPrintOne.findall(type['name']):
                    if (Item_Type.text is not None) and (Item_Type.text != ''):
                        AsString = Item_Type.text
                        AsList = [float(s) for s in AsString.split(',')]
                        AsList = AsList[a_skip_values:]

                        values = []
                        x_absolute = 0
                        y_current = 0
                        for value in AsList:
                            x_absolute += value
                            if type['plot_type'] == 'plot':
                                if type['x_type'] == 'relative':
                                    x = x_absolute
                                    y = value
                                elif type['x_type'] == 'absolute':
                                    x = value
                                    y = y_current
                                    y_current += 1
                                else:
                                    assert(False)
                            elif type['plot_type'] == 'bar':
                                x = value
                                y = 1
                            else:
                                assert (False)

                            values.append({
                                'x': x + (a_file_shift_frames if a_file_shift_frames is not None else 0),
                                'y': y,
                            })

                time_lines_all.append({
                    'subplot_name': a_subplot_name or fingerprint_name or None,
                    'values': values,
                    'plot_label': a_plot_label or type['name'] or None,
                    'plot_type': type['plot_type'],
                    'group': type['group'],
                    'markersize': type.get('markersize', 3),
                    'linewidth': type.get('linewidth', 2),
                    'width': type.get('width', 0.5),
                    'shift': type.get('shift', 0.0),
                    'duration': float(duration),
                    'frames': int(frames)
                })

def show_xml_summary(file_name, a_fingerprint_name=None):
    time_lines_all = []

    types_summary = [
        {'name': "./AsString/Relative/Seconds/Original", 'plot_type': 'plot', 'x_type': 'relative', 'markersize': 7, 'linewidth': 4, 'group': 1},
        {'name': "./AsString/Relative/Seconds/Post_Processed", 'plot_type': 'plot', 'x_type': 'relative', 'markersize': 3, 'linewidth': 2, 'group': 1},
        {'name': "./AsString/Absolute/Seconds/Original", 'plot_type': 'plot', 'x_type': 'absolute', 'markersize': 7, 'linewidth': 4, 'group': 2},
        {'name': "./AsString/Absolute/Seconds/Post_Processed", 'plot_type': 'plot', 'x_type': 'absolute', 'markersize': 3, 'linewidth': 2, 'group': 2},
    ]

    get_time_line(time_lines_all, file_name, a_fingerprint_name, types_summary)

    alpha_show_graphics.show_time_line(time_lines_all, file_name)


def show_xml_compare(file_name_1, file_name_2, a_fingerprint_name=None, a_file_shift_frames_1=0):
    time_lines_all = []

    type_name = "./AsString/Relative/Seconds/Post_Processed"
    types_summary = [{'name': type_name, 'plot_type': 'plot', 'x_type': 'relative', 'markersize': 7, 'linewidth': 4, 'group': 1}]
    get_time_line(time_lines_all, file_name_2, a_fingerprint_name, types_summary, type_name, file_name_2)
                  # a_skip_values=119) #38 238 119
    types_summary = [{'name': type_name, 'plot_type': 'plot', 'x_type': 'relative', 'markersize': 4, 'linewidth': 2, 'group': 1}]
    get_time_line(time_lines_all, file_name_1, a_fingerprint_name, types_summary, type_name, file_name_1, a_file_shift_frames_1)

    type_name = "./AsString/Absolute/Seconds/Post_Processed"
    types_summary = [{'name': type_name, 'plot_type': 'plot', 'x_type': 'absolute', 'markersize': 7, 'linewidth': 4, 'group': 2}]
    get_time_line(time_lines_all, file_name_2, a_fingerprint_name, types_summary, type_name, file_name_2)
    types_summary = [{'name': type_name, 'plot_type': 'plot', 'x_type': 'absolute', 'markersize': 4, 'linewidth': 2, 'group': 2}]
    get_time_line(time_lines_all, file_name_1, a_fingerprint_name, types_summary, type_name, file_name_1, a_file_shift_frames_1)

    type_name = "./AsString/Absolute/Seconds/Post_Processed"
    types_summary = [{'name': type_name, 'plot_type': 'bar', 'x_type': 'absolute', 'width': 0.9, 'shift': 0.0, 'group': 3}]
    get_time_line(time_lines_all, file_name_2, a_fingerprint_name, types_summary, type_name, file_name_2)
    types_summary = [{'name': type_name, 'plot_type': 'bar', 'x_type': 'absolute', 'width': 0.6, 'shift': 0.3, 'group': 3}]
    get_time_line(time_lines_all, file_name_1, a_fingerprint_name, types_summary, type_name, file_name_1, a_file_shift_frames_1)

    alpha_show_graphics.show_time_line(time_lines_all, a_fingerprint_name)


def xml_version_update(a_video_dir):
    print('--------------------')
    print('scanning files...')

    if os.path.isabs(a_video_dir):
        video_dir = a_video_dir
    else:
        video_dir = os.path.join(os.getcwd() + '/' + a_video_dir)

    files_count = 0

    for (dirpath, dirnames, filenames) in os.walk(video_dir):
        print('({} files) in {}'.format(len(filenames), dirpath))

        for file_name in filenames:
            if pathlib.Path(file_name).suffix in ['.xml']:
                files_count += 1
                full_path_xml = os.path.join(dirpath, file_name)

                changed = False

                try:
                    tree = ET.ElementTree(file=full_path_xml)
                    root = tree.getroot()

                    if root.tag == 'Data':
                        if len(root.findall("./Format")) == 0:
                            xml_version_update_none_to_2_0(root, file_name)
                            changed = True
                        elif root.get(__XML_ID_TAG_NAME) is None:
                            xml_version_update_2_to_02_01(root, file_name)
                            changed = True
                        else:
                            Item_Format = find_or_create_item(root, root, ".", "Format")
                            version = Item_Format.get('format_version')

                            if version == '02.01':
                                xml_version_update_02_01_to_02_02(root, file_name)
                                changed = True

                            if version == '02.02':
                                xml_version_update_02_02_to_02_03(root, file_name)
                                changed = True

                    if changed:
                        Item_Format = find_or_create_item(root, root, ".", "Format")
                        Item_Format.set('format_version', __FORMAT_VERSION)

                        tree.write(full_path_xml, encoding="utf-8")
                except Exception as E:
                    print('exception: {}: {}'.format(file_name, str(E)))

    print('--------------------')
    print('total: {} xml files'.format(files_count))


def xml_version_update_none_to_2_0(root, file_name):
    print('     none    -> 2.0: ' + file_name)

    video_stream_index = 0

    Item_Info = find_or_create_item(root, root, ".", "Info")
    root.remove(Item_Info)
    Item_Progress = find_or_create_item(root, root, ".", "Progress")
    root.remove(Item_Progress)
    Item_FingerPrintsAll = find_or_create_item(root, root, ".", "FingerPrintsAll")
    root.remove(Item_FingerPrintsAll)

    Item_Streams = find_or_create_item(root, root, ".", "Streams")
    Item_VideoStream = find_or_create_item(Item_Streams, Item_Streams, ".", "Stream")
    Item_VideoStream.set("index", str(video_stream_index))

    Item_VideoStream.append(Item_Info)
    Item_VideoStream.append(Item_Progress)
    Item_VideoStream.append(Item_FingerPrintsAll)


def xml_version_update_2_to_02_01(root, file_name):
    print('     2       -> 02.01: ' + file_name)

    root.set(__XML_ID_TAG_NAME, __XML_ID_TAG_VALUE)


def xml_version_update_02_01_to_02_02(root, file_name):
    print('    02.01    -> 02.02: ' + file_name)

    for Item_Progress_Stream in root.findall("./Streams/Stream/Progress"):
        Item_Progress_Stream.tag = "Progress_Stream"

    for Item_Progress_FingerPrint in root.findall("./Streams/Stream/FingerPrintsAll/FingerPrintOne/Progress"):
        Item_Progress_FingerPrint.tag = "Progress_FingerPrint"

def xml_version_update_02_02_to_02_03(root, file_name):
    print('    02.02    -> 02.03: ' + file_name)

    for Item_Progress_FingerPrint in root.findall("./Streams/Stream/FingerPrintsAll/FingerPrintOne"):
        Item_Progress_FingerPrint.set('detector_id', Item_Progress_FingerPrint.get('id'))
        Item_Progress_FingerPrint.set('detector_version', Item_Progress_FingerPrint.get('version'))
