import os
from PIL import Image

# 支持的输入图像格式
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp','.jfif'}

# 统一图像格式
def convert_to_png(img_path):
    dir_name = os.path.dirname(img_path)
    file_name_without_ext = os.path.splitext(os.path.basename(img_path))
    prefix_with_name = os.path.join(dir_name, file_name_without_ext[0])

    if file_name_without_ext[1].lower() == '.png':
        print('已经是PNG格式啦')
    if file_name_without_ext[1].lower() not in SUPPORTED_FORMATS:
        return f"跳过不支持的文件格式: {img_path}"
    else:
        try:
            with Image.open(img_path) as image:
                new_path = f"{prefix_with_name}.png"
                image.save(new_path, 'PNG')
                # 删除原图
                os.remove(img_path) 
                print(f"转换成功: {img_path} -> {new_path}")
        except Exception as e:
            print(f"处理文件 {img_path} 时出错: {e}")



# 将文件命名统一为数字
def batch_rename_sequential(folder_path,final_name='test'):
    """
    将文件夹中的文件按 0, 1, 2, 3... 的顺序重命名

    Args:
        folder_path (str): 要处理的文件夹路径
    """
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误：文件夹路径 '{folder_path}' 不存在")
        return
    
    # 获取文件夹中所有项目，并过滤出文件（排除子文件夹）
    all_items = os.listdir(folder_path)
    files = [item for item in all_items if os.path.isfile(os.path.join(folder_path, item))]
    
    # 按原始文件名排序以确保顺序一致性
    files.sort()
    
    # 遍历所有文件并进行重命名
    for index, filename in enumerate(files):
        
        # 获取文件扩展名
        _, ext = os.path.splitext(filename)
        
        # 构建旧文件和新文件的完整路径
        old_file_path = os.path.join(folder_path, filename)
        new_filename = f"{final_name}{index}{ext}" # 新文件名为数字+原扩展名
        new_file_path = os.path.join(folder_path, new_filename)
        
        # 执行重命名操作
        try:
            os.rename(old_file_path, new_file_path)
            print(f"成功：'{filename}' -> '{new_filename}'")
            convert_to_png(new_file_path)

        except Exception as e:
            print(f"重命名 '{filename}' 时出错：{str(e)}")
    print("批量重命名完成！")


path_to_your_folder = r"E:\Coding\AI-LandscapeePlan\data\AI-Plan-数据采集\plan"
batch_rename_sequential(path_to_your_folder)