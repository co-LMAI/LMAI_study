import os
from PIL import Image


def resize_image(image_path, output_path):

    for filename in os.listdir(file_path):
        image_path = os.path.join(file_path, filename)
        output_path = os.path.join(resize_path, filename)
        # 获取图像原始尺寸
        img = Image.open(image_path)

        # 获取新尺寸
        width, height = img.size

        # 缩放图像
        if width > height:
            new_width = 1024
            new_height = int(height * (new_width / width))
            img = img.resize((new_width, new_height))    
        else:
            new_height = 1024
            new_width = int(width * (new_height / height)) 
            img = img.resize((new_width, new_height))
        print(f"已处理图像: {filename}, 新尺寸: {new_width}x{new_height}")
        img.save(output_path)

if __name__ == "__main__":
    
    file_path = r"E:\Desktop\data\output"
    resize_path = r"E:\Desktop\data\resize_output"
    if not os.path.exists(resize_path):
        os.makedirs(resize_path)

    resize_image(file_path, resize_path)

