import os


file_path = r'E:\Desktop\data\edit'


for filename in os.listdir(file_path):
    image_path = os.path.join(file_path, filename)
    print(filename.split('_'))
    strat,end = filename.split('_')
    if end == 'strat.png':
        image_path_new = os.path.join(file_path, strat+'_'+'start.png')
        print(image_path_new)
        os.rename(image_path,image_path_new)
