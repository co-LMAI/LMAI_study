from skimage import io, color, measure
import os
from datasets import Dataset, Image
import numpy as np






class Image_evaluation_dataset:

    def __init__(self,image_path):

        self.image_path = image_path
        self.image_list = [os.path.join(self.image_path,i) for i in os.listdir(self.image_path)]

        self.data_dict = {}
        self.data_dict['image'] = self.image_list
        self.data_dict['entropy'] = [self.get_entropy(i) for i in self.image_list]  

        self.dataset = Dataset.from_dict(self.data_dict).cast_column('image',Image())



    def get_entropy(self,image_path):
        # 读取图像并转为灰度
        image = io.imread(image_path)
        gray = color.rgb2gray(image) if image.ndim == 3 else image

        # 计算香农熵（默认以2为底）
        entropy = measure.shannon_entropy(gray)
        return entropy




file_path = r'E:\Desktop\data\edit_start'

file_dict = {}
file_dict['image'] = []
for i in os.listdir(file_path):
    path =os.path.join(file_path,i)
    file_dict['image'].append(path)

dataset = Dataset.from_dict(file_dict).cast_column('image',Image())
print(dataset[0])