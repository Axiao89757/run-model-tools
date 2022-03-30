'''

'''
import os
import random
import shutil
import argparse
from operator import itemgetter

# 自定义目录名字
second_str1 = 'A'
second_str2 = 'B'
third_str1 = 'train'
third_str2 = 'val'
third_str3 = 'test'

dataset_path = r'E:\datasets\(2017)SSDD\ssddt'
init_files_path = [r'E:\datasets\(2017)SSDD\ssdd\JPEGImages', r'E:\datasets\(2017)SSDD\ssdd\newAnnotations']


# 文件路径结构检查
def check_path_structure(dataset_path):
    print('目录结构检查')
    # 路径
    images_path = os.path.join(dataset_path, second_str1)
    img_train_path = os.path.join(images_path, third_str1)
    img_val_path = os.path.join(images_path, third_str2)
    img_test_path = os.path.join(images_path, third_str3)

    labels_path = os.path.join(dataset_path, second_str2)
    lb_train_path = os.path.join(labels_path, third_str1)
    lb_val_path = os.path.join(labels_path, third_str2)
    lb_test_path = os.path.join(labels_path, third_str3)

    paths = {
        'dataset_root': dataset_path,
        'second1': images_path,
        'second2': labels_path,
        'third11': img_train_path,
        'third12': img_val_path,
        'third13': img_test_path,
        'third21': lb_train_path,
        'third22': lb_val_path,
        'third23': lb_test_path
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
    parser.add_argument('--save_path', required=True, help='数据集保存路径')
    parser.add_argument('--from_path', nargs='+', help='数据集来源，不是重组的情况下必输，第一项是A类，第二项是B类')
    parser.add_argument('-p', '--percent', nargs='+', type=int, required=True, default=[8, 1, 1], help='训练:验证:测试集的比例')
    parser.add_argument('-rd', '--redivide', action="store_true", help='重新分组')
    parser.add_argument('-ft', '--file_type', nargs='+', default=['.jpg', '.png'],
                        help='照片的格式')
    args = parser.parse_args()

    paths = check_path_structure(args.save_path)
    # 获取全部文件的路径
    if args.redivide:
        file_paths = get_all_file_paths(itemgetter(*['third11', 'third12', 'third13'])(paths), args.file_type)
        b_file_paths = [x.replace(second_str1, second_str2) for x in file_paths]
    else:
        file_paths = get_all_file_paths([args.from_path[0]], args.file_type)
        b_file_paths = [os.path.join(args.from_path[1], os.path.split(x)[-1]) for x in file_paths]
    # 排号
    sum_num = len(file_paths)
    id_list = list(range(0, sum_num))
    random.shuffle(id_list)
    # 按比例分组
    percent = {
        'thirdx1': args.percent[0],
        'thirdx2': args.percent[1],
        'thirdx3': args.percent[2]
    }
    rate = sum_num / sum(percent.values())
    thirdx1 = int(percent['thirdx1'] * rate)
    thirdx2 = int(percent['thirdx2'] * rate)

    # 文件迁移 or 复制
    # 验证集
    print('文件搬移（复制）')
    for i in range(0, sum_num):
        if i < thirdx1:
            atp = paths['third11']
            btp = paths['third21']
        elif i < thirdx1 + thirdx2:
            atp = paths['third12']
            btp = paths['third22']
        else:
            atp = paths['third13']
            btp = paths['third23']

        move_if_dif(file_paths[id_list[i]], atp, args.redivide)
        move_if_dif(b_file_paths[id_list[i]], btp, args.redivide)


    # 统计输出
    print('文件个数统计：')
    count_file(paths.values())
    print('结束')
