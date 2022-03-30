import xml.dom.minidom as xmldom
import os
import argparse

# xml_path = r'E:\datasets\(2017)SSDD\SSDD\newAnnotations'
# txt_path = r'E:\datasets\(2017)SSDD\SSDD_ed\labels'

parser = argparse.ArgumentParser()
parser.add_argument('-xp', help='path of xml')
parser.add_argument('-tp', help='path of txt')
args = parser.parse_args()
xml_path = args.xp
txt_path = args.tp

def convert(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def do_one_file(file_name):
    xywh = ''
    xml_file = xmldom.parse(file_name)
    els = xml_file.documentElement
    width = els.getElementsByTagName('width')[0].firstChild.data
    height = els.getElementsByTagName('height')[0].firstChild.data
    for obj in els.getElementsByTagName('object'):
        xmin = obj.getElementsByTagName("xmin")[0].firstChild.data
        xmax = obj.getElementsByTagName("xmax")[0].firstChild.data
        ymin = obj.getElementsByTagName("ymin")[0].firstChild.data
        ymax = obj.getElementsByTagName("ymax")[0].firstChild.data
        xywh = xywh + '0 ' + ' '.join(map(lambda x: '%.6f'%x,
                                       (convert((int(width), int(height)),
                                                (int(xmin), int(xmax), int(ymin), int(ymax)))))) + '\n'
    xywh = xywh[:-1]
    with open(os.path.join(txt_path, file_name.split('.')[0] + '.txt'), 'w+') as f:
        f.write(xywh)


print('convert begin')
os.chdir(xml_path)
i = 0
file_names = os.listdir()
start_fn = file_names[0]
for file_name in file_names:
    do_one_file(file_name)
    i = i + 1
    if i % 200 == 0:
        print(start_fn + " ~ " + file_name + ' done')
        start_fn = file_names[i]
    if i == len(file_names):
        print(start_fn + " ~ " + file_name + ' done')
print('end')
