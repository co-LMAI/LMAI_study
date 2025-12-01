import os


file_path = r"E:\Desktop\data\image"
text_path = r"E:\Desktop\data\text"

for filename in os.listdir(file_path):
    image_path = os.path.join(file_path, filename)