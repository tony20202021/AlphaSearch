import alpha_process_file
import alpha_xml
from Detectors.Lists import alpha_detectors_all

import os
import pathlib
import glob
import xml.etree.ElementTree as ET
import numpy as np
import uuid
from distutils.util import strtobool

priorities_all =  {'none':                             00,
                   'no_xml_file':                      70,
                   'no_data_in_xml_file':              80,
                   'exception_parsing_xml_file':       95,
                   'not_finished':                     10,
                   'not_all_detectors':                20,
                   'old_detector_version':             30,
                   'detector_not_finished':            40,
                   'old_info':                         50,
                   'date_time_exception':              60,
                 }

def process_xml(full_path_video, files_all):
    detectors_all = alpha_detectors_all.get_all_detectors()

    full_path_xml = full_path_video + '.xml'

    need_process = False
    description = 'none'
    need_detectors = []
    steam_count = 0

    if not os.path.exists(full_path_xml):
        need_process = True
        description = 'no_xml_file'
    else:
        try:
            tree = ET.ElementTree(file=full_path_xml)
            root = tree.getroot()

            need_process = True
            description = 'no_data_in_xml_file'

            for Item_Stream in root.findall('./Streams/Stream'):

                stream = Item_Stream.get('index')
                steam_count += 1

                for Item_FingerPrintsAll in Item_Stream.findall('./FingerPrintsAll'):

                    need_process = False
                    description = 'none'

                    for detector_key in detectors_all:
                        for finger_print in detectors_all[detector_key]['detector'].get_finger_prints():

                            found = False
                            for Item_FingerPrintOne in Item_FingerPrintsAll.findall('./FingerPrintOne'):
                                if finger_print['finger_print_name'] == Item_FingerPrintOne.get('name'):
                                    found = True
                                    version = Item_FingerPrintOne.get('detector_version')
                                    if (version is None) or (int(version) < detectors_all[detector_key]['detector'].f_version):
                                        need_process = True
                                        description = 'old_detector_version'
                                        need_detectors.append(detector_key)
                                        break

                                    Item_Progress = Item_FingerPrintOne.findall("./Progress_FingerPrint")[0]
                                    finished = (Item_Progress.get('finished') is not None) and (bool(strtobool(Item_Progress.get('finished'))))
                                    if (not finished):
                                        need_process = True
                                        description = 'detector_not_finished'
                                        need_detectors.append(detector_key)
                                        break

                            if not found:
                                need_process = True
                                description = 'not_all_detectors'
                                need_detectors.append(detector_key)
                                break

                files_all.append({'full_path_video': full_path_video, 'stream': stream,
                                  'need_process': need_process,
                                  'priority': priorities_all[description],
                                  'description': description, 'need_detectors': need_detectors})
        except Exception as E:
            print('exception: {}: {}'.format(full_path_video, str(E)))
            steam_count = 0
            need_process = True
            description = 'exception_parsing_xml_file'

    if steam_count == 0:
        files_all.append({'full_path_video': full_path_video, 'stream': 'none', 'need_process': need_process, 'priority': priorities_all[description], 'description': description, 'need_detectors': need_detectors})

def process_dir(a_video_dir, a_video_ext):
    print('delete temp files...')
    for fl in glob.glob("__temp_raw_(" + "*" + ").raw"):
        os.remove(fl)

    print('scanning files...')

    if os.path.isabs(a_video_dir):
        video_dir = a_video_dir
    else:
        video_dir = os.path.join(os.getcwd() + '/' + a_video_dir)
    video_ext = ['.' + e.lower() for e in a_video_ext.split(',')]

    files_all = []

    detectors_all = alpha_detectors_all.get_all_detectors()

    for (dirpath, dirnames, filenames) in os.walk(video_dir):
        for file_name in filenames:
            if pathlib.Path(file_name).suffix.lower() in video_ext:
                full_path_video = os.path.join(dirpath, file_name)
                process_xml(full_path_video, files_all)

    print('total: {} files in dir:'.format(len(files_all)))
    priorities_found = np.nonzero(np.bincount([f['priority'] for f in files_all if f['need_process']]))[0]

    files_count = len([1 for f in files_all if (not f['need_process'])])
    print('indexed: {:4d} file(s)'.format(files_count))

    if len(priorities_found) == 0:
        print('all files are indexed')
    else:
        print('not indexed:')
        for key in priorities_found:
            files_count = len([1 for f in files_all if (f['priority'] == key)])
            print('priority({:d}): {:4d} file(s) ({})'.format(key, files_count, list(priorities_all.keys())[list(priorities_all.values()).index(key)]))
    print('---------------')

    files_count_all = len([1 for f in files_all if (f['priority'] != 0)])
    file_index = 0
    for p in priorities_found:
        if p != 0:
            print('---------------')
            print('processing priority: {}...'.format(p))
            print('---------------')
            for file in files_all:
                if file['priority'] == p:
                    file_index += 1
                    print('---------------')
                    print('file: {}/{}'.format(file_index, files_count_all))

                    try:
                        full_path_xml = file['full_path_video'] + '.xml'
                        if os.path.exists(full_path_xml):
                            tree = ET.ElementTree(file=full_path_xml)
                            root = tree.getroot()
                        else:
                            root = ET.Element('Data')
                            tree = ET.ElementTree(root)

                        Item_Lock = alpha_xml.find_or_create_item(tree, root, '.', 'Lock')
                        locked = (Item_Lock.get('locked') is not None) and (bool(strtobool(Item_Lock.get('locked'))))
                        lock_id = Item_Lock.get('lock_id')

                        if locked or ((lock_id is not None) and (lock_id != '')):
                            print('locked: {}'.format(full_path_xml))
                            continue

                        lock_id = uuid.uuid4()
                        Item_Lock.set('locked', str(True))
                        Item_Lock.set('lock_id', str(lock_id))
                        tree.write(full_path_xml, encoding="utf-8")
                       
                        files_lock = []
                        process_xml(full_path_video, files_lock)

                        for file_lock in files_lock:
                            if file['priority'] != 0:
                                print('priority: {} ({})'.format(file['priority'], list(priorities_all.keys())[list(priorities_all.values()).index(file['priority'])]))
                                print('---------------')

                                tree = ET.ElementTree(file=full_path_xml)
                                root = tree.getroot()
                                Item_Lock = alpha_xml.find_or_create_item(tree, root, '.', 'Lock')
                                lock_id_new = Item_Lock.get('lock_id')
                                if (str(lock_id) != lock_id_new):
                                    print('locked: {}'.format(full_path_xml))
                                    continue

                                alpha_process_file.process_file(file['full_path_video'], 'process_dir', 0, file['need_detectors'])

                                tree = ET.ElementTree(file=full_path_xml)
                                root = tree.getroot()
                                for Item_Lock in root.findall('./Lock'):
                                    Item_Lock.set('locked', str(False))
                                    Item_Lock.set('lock_id', str(''))
                                tree.write(full_path_xml, encoding="utf-8")

                    except Exception as E:
                        print('exception: {}: {}'.format(file['full_path_video'], str(E)))

                    print('---------------')


def clear_locks(a_video_dir):
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

                try:
                    tree = ET.ElementTree(file=full_path_xml)
                    root = tree.getroot()

                    for Item_Lock in root.findall('./Lock'):
                        locked = (Item_Lock.get('locked') is not None) and (bool(strtobool(Item_Lock.get('locked'))))
                        lock_id = Item_Lock.get('lock_id')
                        if locked or ((lock_id is not None) and (lock_id != '')):
                            Item_Lock.set('locked', str(False))
                            Item_Lock.set('lock_id', str(''))
                            tree.write(full_path_xml, encoding="utf-8")
                            print('unlocked: {}'.format(full_path_xml))

                except Exception as E:
                    print('exception: {}: {}'.format(file_name, str(E)))

    print('--------------------')
    print('total: {} xml files'.format(files_count))





