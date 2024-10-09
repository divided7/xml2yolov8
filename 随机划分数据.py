import os
import shutil
import random
import argparse
from tqdm import tqdm


# 复制文件函数，添加 tqdm 进度条
def copy_files(data, img_dst_dir, label_dst_dir):
    for img_file, label_file in tqdm(data, desc=f"Copying files to {img_dst_dir}"):
        img_src = os.path.join(shot_dir, img_file)
        label_src = os.path.join(shot_dir, label_file)

        # 检查图片和标签文件是否存在
        if os.path.exists(img_src) and os.path.exists(label_src):
            # 复制图片
            shutil.copy(img_src, img_dst_dir)
            # 复制标签
            shutil.copy(label_src, label_dst_dir)


if __name__ == "__main__":
    # 使用 argparse 解析命令行参数
    parser = argparse.ArgumentParser(
        description="YOLO数据集随机划分, 用于将存在于路径`shot_dir`下的图片和txt随机划分到shot_dir/images/train, shot_dir/images/val, shot_dir/labels/train, shot_dir/labels/val")
    parser.add_argument('--shot_dir', type=str, default='shot', help='Source directory for images and labels')
    parser.add_argument('--images_dir', type=str, default='images', help='Target directory for images')
    parser.add_argument('--labels_dir', type=str, default='labels', help='Target directory for labels')
    parser.add_argument('--train_ratio', type=float, default=0.8, help='Proportion of training data (0-1)')

    args = parser.parse_args()

    # 文件路径定义
    shot_dir = args.shot_dir
    images_dir = args.images_dir
    labels_dir = args.labels_dir

    # 创建训练集和验证集的文件夹结构
    train_img_dir = os.path.join(images_dir, 'train')
    val_img_dir = os.path.join(images_dir, 'val')
    train_label_dir = os.path.join(labels_dir, 'train')
    val_label_dir = os.path.join(labels_dir, 'val')

    # 创建文件夹
    os.makedirs(train_img_dir, exist_ok=True)
    os.makedirs(val_img_dir, exist_ok=True)
    os.makedirs(train_label_dir, exist_ok=True)
    os.makedirs(val_label_dir, exist_ok=True)

    # 划分比例
    train_ratio = args.train_ratio
    val_ratio = 1 - train_ratio

    # 获取 shot 目录下的所有图片和对应标签文件
    image_files = [f for f in os.listdir(shot_dir) if f.endswith(('.jpg', '.png'))]
    label_files = [f.replace('.jpg', '.txt').replace('.png', '.txt') for f in image_files]

    # 随机划分数据集
    data_pairs = list(zip(image_files, label_files))
    random.shuffle(data_pairs)

    # 计算训练集和验证集数量
    train_size = int(len(data_pairs) * train_ratio)
    train_data = data_pairs[:train_size]
    val_data = data_pairs[train_size:]

    # 复制训练集文件
    copy_files(train_data, train_img_dir, train_label_dir)

    # 复制验证集文件
    copy_files(val_data, val_img_dir, val_label_dir)

    print(f"数据集划分完成：训练集 {len(train_data)} 个，验证集 {len(val_data)} 个。")
