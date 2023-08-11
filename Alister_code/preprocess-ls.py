# ==============================================================================
# Binaries and/or source for the following packages or projects 
# are presented under one or more of the following open source licenses:
# preprocess.py    The OpenLane-V2 Dataset Authors    Apache License, Version 2.0
#
# Contact wanghuijie@pjlab.org.cn if you have any issue.
#
# Copyright (c) 2023 The OpenLane-v2 Dataset Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================='


import numpy as np
import matplotlib.pyplot as plt

from openlanev2.centerline.io import io
from openlanev2.lanesegment.preprocessing import collect
from openlanev2.lanesegment.dataset import Collection, Frame
from openlanev2.lanesegment.visualization import draw_annotation_pv, assign_attribute, assign_topology
import glob
import os
import cv2

#frame = collection.get_frame_via_identifier(('train', '00492', '315970276749927222'))
def analysis_frame(frame, id, c, save_img=False):
    #for k in frame.get_camera_list():
    #    print(k)

    camera = frame.get_camera_list()[0]

    image = frame.get_rgb_image(camera)

    meta = {
        'intrinsic': frame.get_intrinsic(camera),
        'extrinsic': frame.get_extrinsic(camera),
    }
    #for key, value in meta.items():
    #    for k, v in value.items():
    #        print(key, '-', k, '\n', v, '\n')

    annotations = frame.get_annotations()
    #print("annotations:{}".format(annotations))
    print("annotations:{}".format(annotations.keys()))
    print(list(annotations.keys()))

    # for a, anno in zip(
    #     ['lane_segment', 'traffic_element', 'area', 'topology_lsls', 'topology_lste'], 
    #     [
    #         frame.get_annotations_lane_segments()[0],
    #         frame.get_annotations_traffic_elements()[0],
    #         frame.get_annotations_areas()[0],
    #         frame.get_annotations_topology_lsls(),
    #         frame.get_annotations_topology_lste(),
    #     ]):
    #     print(f'\n{a}:')
    #     if isinstance(anno, dict):
    #         for k, v in anno.items():
    #             print(k, v.shape) if isinstance(v, np.ndarray) else print(k, type(v))
    #     else:
    #         print('adjacent matrix', anno.shape)
    have_anno=False
    for i in annotations.keys():
        if i=='topology_lste':
            have_anno=True
    print("have_anno :{}".format(have_anno))
    if have_anno:
        annotations = assign_attribute(annotations)
        annotations = assign_topology(annotations)

        image_pv_laneline, c = draw_annotation_pv(
            camera, 
            image.copy(), 
            annotations,
            meta['intrinsic'],
            meta['extrinsic'],
            with_attribute=False,
            with_linetype=True,
            with_topology=False,
            with_centerline=False, 
            with_laneline=True,
            with_area=False,
            save_img=save_img, #Alister add
            id=id,
            c=c #Alister add
        )
        show_plot=False
        use_opencv=False
        if show_plot:
            if use_opencv:
                cv2.imshow("img",image_pv_laneline)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()
            else:
                plt.figure(figsize=[16, 9])
                plt.subplot(1, 2, 2).imshow(image_pv_laneline)
                plt.subplot(1, 2, 1).imshow(image)
                #plt.subplot(1, 3, 1).imshow(image_pv_centerline)
                #plt.subplot(1, 3, 2).imshow(image_pv_laneline)
                #plt.subplot(1, 3, 3).imshow(image_pv_area)
                plt.show()
        return c
    else:
        print("missing topology_lste ... ")
        return c

def parse_path(path):
    #path format : ./data/OpenLane-V2/train/00025/info/315972374649927217.json
    #Purpose : we need to parse the path, get the "00025" and "315972374649927217"
    file = path.split("/")[-1]
    img_name = file.split(".")[0]
    img_name = img_name.split("-")[0]
    id = path.split("/")[-3]
    return id, img_name

if __name__=="__main__":
    with_sd_map = False # TODO: include SD Maps as sensor inputs or not
    root_path = './data/OpenLane-V2'
    file = "data_dict_sample.json"
    subset = 'train'
    # for file in io.os_listdir(root_path):
    #     if file.endswith('json'):
    #         subset = file.split('.')[0]
    for split, segments in io.json_load(f'{root_path}/{file}').items():
        collect(
            root_path, 
            {split: segments}, 
            f'{subset}_{split}_ls' if not with_sd_map else f'{subset}_{split}_ls_sd',
            with_sd_map = with_sd_map,
            n_points={
                'area': 20,
                'centerline': 10,
                'left_laneline': 20,
                'right_laneline': 20,
            },
        )
    #Need to preprocess first
    collection = Collection(root_path, root_path, 'data_dict_sample_train_ls')

    label_dir = "./data/OpenLane-V2/train/"
    #train/id/image/type/xxxx..jpg
    label_path_list = glob.glob(os.path.join(label_dir,'***','**','*.json'))

    #Parsing images and save landmark ROI images
    print("Parsing images and save landmark ROI images")
    c = 1
    for i in range(len(label_path_list)):
        print(label_path_list[i])
        id,img_name = parse_path(label_path_list[i])
        print("id={}, img_name={}".format(id,img_name))
        try:
            frame = collection.get_frame_via_identifier(('train', id, img_name))
            print("start analysis_frame")
            c = analysis_frame(frame, id, c, save_img=True)
        except:
            print("Error pass!")
            pass
        



