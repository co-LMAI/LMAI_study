import os


file_path = r'C:\Users\2022169\Desktop\data\图像编辑'


for filename in os.listdir(file_path):
    image_path = os.path.join(file_path, filename)

    strat,mid,end = filename.split('_')
    if end == 'end.png':
        image_path_new = os.path.join(file_path, mid+'_'+'strat.png')
        print(image_path_new)
        os.rename(image_path,image_path_new)

    if end == 'strat.png':
        image_path_new = os.path.join(file_path, mid+'_'+'end.png')
        print(image_path_new)
        os.rename(image_path,image_path_new)      

    if end == 'end.txt':
        image_path_new = os.path.join(file_path, mid+'.txt')
        print(image_path_new)
        os.rename(image_path,image_path_new)
    