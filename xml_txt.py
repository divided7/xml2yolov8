# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os

classes = ['person'] # 这里classes根据实际情况替换, 例如coco数据集要按顺序替换为[person, ...] 共80个


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


path = r'C:\Users\UangSC\Desktop\IDM\20240826_50m_552张'  # 路径
for file in os.listdir(path):
    if file.endswith('.xml'):
        xml_path = os.path.join(path, file)
        txt_path = xml_path[:-4] + '.txt'
        # if not os.path.exists(txt_path):
        #     os.mkdir(txt_path)
        # print(jpg_path)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            cls = obj.find('name').text
            # print(cls)
            # if cls!='person':
            #     continue
            if cls not in classes:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            xmin = float(xmlbox.find('xmin').text)
            xmax = float(xmlbox.find('xmax').text)
            ymin = float(xmlbox.find('ymin').text)
            ymax = float(xmlbox.find('ymax').text)
            x = (xmin + xmax) / 2 / w
            y = (ymin + ymax) / 2 / h
            width = (xmax - xmin) / w
            height = (ymax - ymin) / h

            # if x > 1 or y > 1 or width > 1 or height > 1:
            #     print(file)
            with open(txt_path, 'a+') as f:
                # f.write(str(3) + ' ' + str(x) + ' ' + str(y) + ' ' + str(width) + ' ' + str(height) + '\n')
                f.write(str(cls_id) + ' ' + str(x) + ' ' + str(y) + ' ' + str(width) + ' ' + str(height) + '\n')
