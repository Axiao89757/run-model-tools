
一个为跑模型而生的工具箱

# 1. 把.xml标签文件转为.txt文件
.xml文件示例
```xml
<?xml version="1.0" ?><annotation verified="no">
  <folder>JPEGImages</folder>
  <filename>000017.jpg</filename>
  <path>K:\newmodel\SARShip\dataset\Annotations</path>
  <source>
    <database>Unknown</database>
  </source>
  <size>
    <width>500</width>
    <height>354</height>
    <depth>1</depth>
  </size>
  <segmented>0</segmented>
  <object>
    <name>ship</name>
    <pose>Unspecified</pose>
    <truncated>0</truncated>
    <difficult>0</difficult>
    <bndbox>
      <xmin>82</xmin>
      <ymin>224</ymin>
      <xmax>135</xmax>
      <ymax>241</ymax>
    </bndbox>
  </object>
  <object>
    <name>ship</name>
    <pose>Unspecified</pose>
    <truncated>0</truncated>
    <difficult>0</difficult>
    <bndbox>
      <xmin>360</xmin>
      <ymin>108</ymin>
      <xmax>416</xmax>
      <ymax>129</ymax>
    </bndbox>
  </object>
</annotation>
```
.txt文件示例
```txt
0 0.217000 0.656780 0.106000 0.048023
0 0.776000 0.334746 0.112000 0.059322
```
转换
```bash
python xml2txt.py -xp E:\newAnnotations -tp E:\labels
# -xp：.xml文件的父目录
# -tp: .txt文件的存储目录
```
# 2. 划分数据集(yolov5)
方式一：重分。文件移动的方式
```bash
python dvdata.py -dp E:\grouped -p 8 1 1 -rd
```
```
# -dp：数据集的路径
# -p：训练集 : 验证集 : 测试集
# -rd：在该数据集下重新划分
```
方式二：初始划分。文件复制的方式
```bash
python dvdata.py -dp E:\grouped -dps E:\JPEGImages E:\newAnnotations -p 8 1 1
```
```
# -dp：数据集的路径
# -dps：数据所在目录
# -p：训练集 : 验证集 : 测试集
```
指定照片、标签文件类型
```bash
python dvdata.py -dp E:\grouped -dps E:\JPEGImages E:\newAnnotations -p 8 1 1 -ft .jpg .txt
```
```
# -dp：数据集的路径
# -dps：数据所在目录
# -p：训练集 : 验证集 : 测试集
```
# 3. 划分数据集(pix2pix)
方式一：重新划分。文件移动的方式
```bash
python datapp_pix2pix.py --save_path C:\Users\22132\Desktop\ddddsave --redivide -p 8 1 0
```
```
# --save_path：划分后的数据集保存路径
# --redivide：重新划分
# -p：训练集 : 验证集 : 测试集
```
方式二：初始划分。文件复制的方式
```bash
python datapp_pix2pix.py --save_path C:\save --from_path C:\hh C:\ee -p 9 1 0
```
```
# --save_path：划分后的数据集保存路径
# --from_path：数据来源，两个路径，其下的文件名需一样
# -p：训练集 : 验证集 : 测试集
```
# 4. 划分数据集（SSD）
SSD算法的数据集划分相对简单，需要的图像文件放在JPEGImages下，标签文件格式为.xml，其放在Annotations下。
此外，需要创建四个数据集文件名划分txt文件（text.txt train.txt val.txt trainval.txt），放在ImageSets\Mian下，目录结构如下：

```
|_dataset_root
    |_Annotations       # 原始.xml标注文件
    |_JPEGImages        # 图像文件
    |_ImageSets         # ssd数据集的说明文件
    |_Main<br>
        |_test.txt          # 测试集的文件名文件 001,002,003
        |_train.txt         # 训练集的文件名文件
        |_trainval.txt      # 训练集和验证集的文件名文件
        |_val.txt           # 验证集的文件名文件
        
tips: 其中Annotations和JPEGImages需要提前创建好，并且将图片和标注文件放进去
```
命令
```bash
python imagesets.py --dataset-path E:\SSDD_init --percent 7 2 1
```
```bash
# --dataset-path 数据集的根目录
# --percent 训练集:验证集:测试集
```
# 5. 为图像画框
在拥有.xml标注文件和图像文件的情况下，
但此时图像只是原始的图像，并没有画出标注框，即可使用此工具画出来。**注意：.txt标注文件暂不支持**
1. 直接画出给出的文件目录下的全部标注，默认是标签目录
    ```bash
   python label2img.py --label-path E:\xml-label --img-path E:\JPEGImages --save-path E:\save --color 0 0 256 --thick 2
   ```
   ```
   # --label-path：标签文件所在目录
   # --img-path：图像所在目录
   # --from-img：以图像所在目录的文件名作为画框标准，默认是标签目录
   # --color：框的颜色（R，G，B）
   # --clear-dir：清空保存目录的原本内容
   # --thick：框的厚度
   ```
   
2. txt说明文件指明需要画哪些标注
   ```bash
   python label2img.py --label-path E:\Annotations --img-path E:\JPEGImages --save-path E:\save --choose-txt E:\test.txt
   ```
   ```
   # --choose-txt；待画标签文件描述文件路径
   ```

# 其他工具
## 1. 从txt描述文件里选择对应img文件复制到指定路径
.txt描述文件。每一行表示一个文件名，不包含后缀的文件名
```
000733
000189
000846
000114
000049
000221
000145
000378
000831
000588
000797
```
命令
```bash
python choosefile.py --txt-path E:\test.txt --img-dir E:\JPEGImages --save-dir E:\test-move
```
```
# --txt-path：描述txt文件的路径
# --img-dir：图片所在目录：
# --save-dir：保存文件目录
# --clear-dir：在保存文件之前，清空原有的文件
```