# 从txt描述文件里选择对应的文件复制到指定路径

import os
import argparse
import shutil

if __name__ == '__main__':
    print('start')
    parser = argparse.ArgumentParser()
    parser.add_argument('--txt-path', required=True, help='描述txt文件的路径')
    parser.add_argument('--img-dir', required=True, help='欲复制的文件所在目录')
    parser.add_argument('--save-dir', required=True, help='保存文件目录')
    parser.add_argument('--clear-dir', action='store_true', default=True, help='在保存文件之前，清空原有的文件')
    args = parser.parse_args()
    txt_path = args.txt_path
    img_dir = args.img_dir
    save_dir = args.save_dir
    clear_dir = args.clear_dir

    # 读取文件名（无后缀）
    if os.path.isfile(txt_path):
        with open(txt_path, 'r') as f:
            filenames = f.read().split('\n')
            print('files: ', len(filenames))
            # 复制文件
            if os.path.exists(save_dir):
                files = os.listdir(save_dir)
                if clear_dir and len(files) > 0:
                    for fn in files:
                        os.remove(os.path.join(save_dir, fn))
            else:
                os.makedirs(save_dir)
            for filename in filenames:
                suffix = os.path.splitext(os.listdir(img_dir)[0])[-1]
                source = os.path.join(img_dir, filename + suffix)
                shutil.copy(source, save_dir)
    print('saved:', save_dir)
    print('end')
