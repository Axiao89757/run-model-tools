# 将 xml 标签文件画到img上
import argparse
import cv2
import os
import xml.etree.cElementTree as ET


def get_bbox(label_path):
    file_type = os.path.splitext(label_path)[-1]
    object_bbox = list()
    if file_type == '.xml':
        tree = ET.ElementTree(file=label_path)
        root = tree.getroot()
        object_set = root.findall('object')
        for Object in object_set:
            bbox = Object.find('bndbox')
            x1 = int(bbox.find('xmin').text.split('.')[0])
            y1 = int(bbox.find('ymin').text.split('.')[0])
            x2 = int(bbox.find('xmax').text.split('.')[0])
            y2 = int(bbox.find('ymax').text.split('.')[0])
            obj_bbox = [x1, y1, x2, y2]  # 若要加上标签，则这里加上物体名字即可
            object_bbox.append(obj_bbox)
    elif file_type == '.txt':
        with open(label_path, 'r') as f:
            data = f.read()
            lines = data.split('\n')
            for line in lines:
                box = line.split(' ')[1:]
                x = float(box[0])
                y = float(box[1])
                w = float(box[2])
                h = float(box[3])
                x1 = x - w / 2
                y1 = y - h / 2
                x2 = x + w / 2
                y2 = y + h / 2
                obj_bbox = [x1, y1, x2, y2]
                object_bbox.append(obj_bbox)
    else:
        raise Exception('标签文件类型错误')
    return object_bbox


def drow_object(img_file, bndboxes, save_path, label_type):
    img = cv2.imread(img_file)
    filename = os.path.split(img_file)[-1]
    for i in range(len(bndboxes)):
        xmin = bndboxes[i][0]
        ymin = bndboxes[i][1]
        xmax = bndboxes[i][2]
        ymax = bndboxes[i][3]
        if label_type == '.xml':
            cv2.rectangle(img, (xmin, ymax), (xmax, ymin), (0, 0, 255), 2)
        elif label_type == '.txt':
            # 获取图片长宽
            w = img.shape[0]
            h = img.shape[1]
            xmin = int(xmin * w)
            ymin = int(ymin * h)
            xmax = int(xmax * w)
            ymax = int(ymax * h)
            cv2.rectangle(img, (xmin, ymax), (xmax, ymin), (0, 0, 255), 2)
        else:
            raise Exception('file type err')
    cv2.imwrite(os.path.join(save_path, filename), img)


if __name__ == '__main__':
    print('start')

    # 参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--label-path', required=True, help="标签文件所在目录")
    parser.add_argument('--img-path', required=True, help="对应的图像所在目录")
    parser.add_argument('--from-img', action='store_true', help="以图像所在目录的文件名作为画框队形，默认是标签目录")
    parser.add_argument('--save-path', required=True, help="生成的图像保存位置")
    parser.add_argument('--choose-txt', default=False, help="指定画图的文件名的txt文件，不包后缀，每个文件名占单独一行")
    args = parser.parse_args()
    label_path = args.label_path
    img_path = args.img_path
    from_img = args.from_img
    save_path = args.save_path
    choose_txt = args.choose_txt

    filenames = []
    # 待画图文件名收集，不包后缀
    if choose_txt:  # 从文件名txt读取待画标签名
        with open(choose_txt, 'r') as f:
            filenames = f.read().split('\n')
        print('from description .txt file: ', len(filenames))
    else:  # 从路径直接读取标签名
        for file in os.listdir(label_path if from_img else img_path):
            filenames.append(os.path.splitext(file)[0])
        print('from dir file list: ', len(filenames))

    # 画图
    for fn in filenames:
        label_type = os.path.splitext(os.listdir(label_path)[0])[-1]
        bndboxes = get_bbox(label_path=os.path.join(label_path, fn + label_type))
        drow_object(img_file=os.path.join(img_path, fn + os.path.splitext(os.listdir(img_path)[0])[-1]),
                    bndboxes=bndboxes, save_path=save_path, label_type=label_type)

    print('save to' + save_path)
    print('end')
