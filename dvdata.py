import os
import random
import shutil
import argparse

# 自定义目录名字
pic_str = 'images'
label_str = 'labels'
train_str = 'train'
val_str = 'val'
test_str = 'test'

dataset_path = r'E:\datasets\(2017)SSDD\ssddt'
init_files_path = [r'E:\datasets\(2017)SSDD\ssdd\JPEGImages', r'E:\datasets\(2017)SSDD\ssdd\newAnnotations']


# 文件路径结构检查
def check_path_structure(dataset_path):
    print('目录结构检查')
    # 路径
    images_path = os.path.join(dataset_path, pic_str)
    img_train_path = os.path.join(images_path, train_str)
    img_val_path = os.path.join(images_path, val_str)
    img_test_path = os.path.join(images_path, test_str)

    labels_path = os.path.join(dataset_path, label_str)
    lb_train_path = os.path.join(labels_path, train_str)
    lb_val_path = os.path.join(labels_path, val_str)
    lb_test_path = os.path.join(labels_path, test_str)

    paths = {
        'dataset_root': dataset_path,
        'images': images_path,
        'labels': labels_path,
        'img_train': img_train_path,
        'img_val': img_val_path,
        'img_test': img_test_path,
        'lb_train': lb_train_path,
        'lb_val': lb_val_path,
        'lb_test': lb_test_path
    }

    # 检查与补充
    for path in paths.values():
        if not os.path.exists(path):
            os.mkdir(path)

    return paths


# 全部文件获取
def get_all_file_paths(file_parent_paths, file_suffixs):
    file_paths = []
    for path in file_parent_paths:
        if os.path.exists(path):
            for file_name in os.listdir(path):
                if os.path.splitext(file_name)[-1] in file_suffixs:
                    file_paths.append(os.path.join(path, file_name))
    return file_paths


# 筛选数组元素，根据尾缀
def filtrate_list(l, suffix):
    return [path for path in l if os.path.splitext(path)[-1] == suffix]


# 移动文件，如果位置不一样
def move_if_dif(sn, tp, redivide):
    if os.path.split(sn)[0] != tp:
        if redivide:
            shutil.move(sn, tp)
        else:
            shutil.copy(sn, tp)


# 从源分
def divide(soruce_paths):
    get_all_file_paths(soruce_paths, ['.jpg', '.txt'])


# 统计输出各个文件夹的文件数目
def count_file(paths):
    for p in paths:
        print(p + ': ' + str(len(os.listdir(p))))


if __name__ == '__main__':
    print('开始')
    # 参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-dp', '--dataset_path', required=True, help='数据集保存路径')
    parser.add_argument('-p', '--percent', nargs='+', type=int, required=True, default=[8, 1, 1], help='训练:验证:测试集的比例')
    parser.add_argument('-rd', '--redivide', action="store_true", help='重新分组')
    parser.add_argument('-dps', '--dataset_paths', nargs='+', help='数据的父路径，可以是多个，在不是重分组的情况下必输')
    parser.add_argument('-ft', '--file_type', nargs='+', default=['.jpg', '.txt'],
                        help='照片和标签的类型（后缀名）')
    args = parser.parse_args()

    paths = check_path_structure(args.dataset_path)
    # 获取全部文件的路径
    if args.redivide:
        file_paths = get_all_file_paths(paths.values(), args.file_type)
    else:
        file_paths = get_all_file_paths(args.dataset_paths, args.file_type)
    # 分组
    img_file_paths = filtrate_list(file_paths, args.file_type[0])
    txt_file_paths = filtrate_list(file_paths, args.file_type[1])
    # 排序
    img_file_paths.sort(key=lambda x: os.path.split(x)[-1])
    txt_file_paths.sort(key=lambda x: os.path.split(x)[-1])
    # 排号
    sum_num = len(img_file_paths)
    id_list = list(range(0, sum_num))
    random.shuffle(id_list)
    # 按比例分组
    percent = {
        'train': args.percent[0],
        'val': args.percent[1],
        'test': args.percent[2]
    }
    rate = sum_num / sum(percent.values())
    val_num = int(percent['val'] * rate)
    train_num = int(percent['train'] * rate)

    # 文件迁移 or 复制
    # 验证集
    print('文件搬移（复制）')
    for i in range(0, sum_num):
        if i < train_num:
            move_if_dif(img_file_paths[id_list[i]], paths['img_train'], args.redivide)
            move_if_dif(txt_file_paths[id_list[i]], paths['lb_train'], args.redivide)
        elif i < train_num + val_num:
            move_if_dif(img_file_paths[id_list[i]], paths['img_val'], args.redivide)
            move_if_dif(txt_file_paths[id_list[i]], paths['lb_val'], args.redivide)
        else:
            move_if_dif(img_file_paths[id_list[i]], paths['img_test'], args.redivide)
            move_if_dif(txt_file_paths[id_list[i]], paths['lb_test'], args.redivide)

    # 统计输出
    print('文件个数统计：')
    count_file(paths.values())
    print('结束')
