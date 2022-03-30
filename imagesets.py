import os
import random
import argparse

Annotations_str = 'Annotations'
JPEGImages_str = 'JPEGImages'
ImageSets_str = 'ImageSets'
Main_str = 'Main'

def check_path(dataset_path):
    # 文件路径拼接
    JPEGImages_path = os.path.join(dataset_path, JPEGImages_str)
    Annotations_path = os.path.join(dataset_path, Annotations_str)
    Main_path = os.path.join(dataset_path, ImageSets_str, Main_str)
    # 检查文件路径
    if not os.path.exists(dataset_path) :
        print('错误：' + dataset_path + '不存在')
        return False
    elif not os.path.exists(JPEGImages_path):
        print('错误：' + JPEGImages_path + '不存在')
        return False
    elif not os.path.exists(Annotations_path):
        print('错误：' + Annotations_path + '不存在')
        return False
    else:
        if not os.path.exists(Main_path):
            os.makedirs(Main_path)
        return JPEGImages_path, Annotations_path, Main_path

if __name__ == '__main__':
    print('开始')
    # 参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-path', required=True, help='数据集路径')
    parser.add_argument('-p', '--percent', nargs='+', type=int, required=True, default=[7, 2, 1], help='训练:验证:测试集的比例')
    args = parser.parse_args()
    # 路径检查
    paths = check_path(args.dataset_path)
    # 创建文件并写入
    if paths:
        filenames = os.listdir(paths[0])
        # 排号
        sum_num = len(filenames)
        id_list = list(range(0, sum_num))
        random.shuffle(id_list)
        # 按比例分组
        percent = {
            'train': args.percent[0],
            'val': args.percent[1],
            'test': args.percent[2]
        }
        rate = sum_num / sum(percent.values())
        train_num = int(percent['train'] * rate)
        val_num = int(percent['val'] * rate)

        # 文件名数组准备
        test = []
        train = []
        val = []
        trainval = []
        for i in range(0, sum_num):
            file_str = os.path.splitext(os.path.split(filenames[id_list[i]])[-1])[0]
            if i < train_num:
                train.append(file_str)
                trainval.append(file_str)
            elif i < train_num + val_num:
                val.append(file_str)
                trainval.append(file_str)
            else:
                test.append(file_str)

        # 文件写入
        with open(os.path.join(paths[2], 'test.txt'), 'w') as f:
            f.write('\n'.join(test))
        with open(os.path.join(paths[2], 'train.txt'), 'w') as f:
            f.write('\n'.join(train))
        with open(os.path.join(paths[2], 'val.txt'), 'w') as f:
            f.write('\n'.join(val))
        with open(os.path.join(paths[2], 'trainval.txt'), 'w') as f:
            f.write('\n'.join(trainval))

        # 打印分组情况
        print('train：', len(train))
        print('test：', len(test))
        print('val：', len(val))
        print('trainval：', len(trainval))

    print('结束')






