import json
import yaml
import numpy as np
import os
import matplotlib.colors as mcolors
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from collections import defaultdict




class ISATConverter:
    def __init__(self,json_file_path=None, output_dir=None, yaml_path=None):

        self.json_file_path = json_file_path
        self.output_dir = output_dir
        self.colors = self._load_colors(yaml_path) if yaml_path else {}

    def _load_colors(self, yaml_path):
        """从YAML加载颜色映射"""
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return {
                    item["name"]: item["color"]
                    for item in data.get("label", [])
                    if isinstance(item, dict) and "name" in item and "color" in item
                }
        except Exception as e:
            print(f"加载颜色映射失败: {e}")
            return {}

    def get_color(self, name, default_color=None):
        """安全获取颜色值"""
        return mcolors.to_rgb(self.colors.get(name, default_color or (0, 0, 0)))

    def read_json(self):
        """读取ISAT格式的JSON文件"""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"读取JSON文件失败: {e}")
            return None

    def make_output_dir(self):
        """创建输出目录"""
        if self.output_dir and not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True) 

    def isat_to_png(self):
        """
        为每个类别生成单独的PNG图像
        """
        # 首先归类标注对象
        categories = self.categorize_annotations()
        if not categories:
            return []     

        data = self.read_json()
        if data is None:    
            return '读取JSON失败，无法转换'  

        # 获取基本信息
        image_height = data.get('info', {}).get('height', 0)
        image_width = data.get('info', {}).get('width', 0)

        if image_width <= 0 or image_height <= 0:
            print(f"警告: 图像尺寸无效 ({image_width}x{image_height})，使用默认尺寸1024x1024")
            image_width, image_height = 1024, 1024
        

        
        categories_to_draw = ['外部环境','草地','铺装','广场','活动场地','水景','建筑','小品','植物']  # 可根据需要修改
        # 如果指定了要绘制的类别，则过滤类别
        if categories_to_draw is not None:
            # 过滤出存在的类别
            filtered_categories = {}
            for category in categories_to_draw:
                if category in categories:
                    filtered_categories[category] = categories[category]
                else:
                    print(f"警告: 类别 '{category}' 不存在，已跳过")
            
            if not filtered_categories:
                print("错误: 指定的类别都不存在，无法生成图像")
                return []
            
            categories = filtered_categories
            print(f"将绘制以下类别: {list(categories.keys())}")

        # 创建matplotlib图形
        dpi = 100
        fig, ax = plt.subplots(figsize=(image_width/dpi, image_height/dpi), dpi=dpi)
        ax.set_xlim(0, image_width)
        ax.set_ylim(image_height, 0)  # 注意：图像坐标系与数学坐标系y轴方向相反
        ax.axis('off')  # 隐藏坐标轴
        
        # 设置背景
        ax.set_facecolor(None)  # 透明背景
        # 添加白色背景矩形
        ax.add_patch(patches.Rectangle((0, 0), image_width, image_height, facecolor='white', edgecolor='none', zorder=0))
        # 为每个类别创建图像
        for category_name, annotations in categories.items():

            # 获取类别颜色
            color = self.get_color(category_name, default_color=(0, 0, 0))
            
            # 绘制该类别的所有标注
            for annotation in annotations:
                segmentation = annotation.get('segmentation', [])
                self._draw_polygon(ax, segmentation, color)
            
        # 保存PNG图像
        self.make_output_dir()
        output_filename = f"{os.path.splitext(os.path.basename(self.json_file_path))[0]}.png"
        output_path = os.path.join(self.output_dir, output_filename)
        
        plt.tight_layout(pad=0)
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close()
        
        print(f"PNG图像已保存: {output_path}")

        return  output_path

    def categorize_annotations(self):
        """
        将标注对象按照类别进行归类
        
        返回:
        categories: 字典，键为类别名，值为该类别的所有标注对象列表
        """
        data = self.read_json()
        if data is None:
            print("无法读取JSON文件，无法进行归类")
            return {}
        
        # 使用defaultdict自动创建空列表
        categories = defaultdict(list)
        annotations = data.get('objects', [])
        
        for annotation in annotations:
            category_name = annotation.get('category', '未知类别')
            categories[category_name].append(annotation)
        
        # 打印归类结果
        print("=" * 50)
        print("标注对象归类结果:")
        print("=" * 50)
        for category, annotations in categories.items():
            print(f"类别 '{category}': {len(annotations)} 个标注对象")
        print("=" * 50)
        
        return dict(categories)  # 转换为普通字典返回

    def _draw_polygon(self, ax, segmentation, color):
        """绘制多边形到matplotlib轴对象"""
        try:
            # 确保segmentation是列表的列表
            if segmentation and isinstance(segmentation[0], (int, float)):
                segmentation = [segmentation]

            polygon = patches.Polygon(segmentation, fill=True, color=color, alpha=1.0, linewidth=0)
            ax.add_patch(polygon)

        except Exception as e:
            print(f"绘制多边形失败: {e}")
            
    def batch_convert(self, json_dir):
            """
            批量转换目录中的所有JSON文件
            
            参数:
            json_dir: 包含JSON文件的目录路径
            categories_to_draw: 要绘制的类别列表，如果为None则使用默认列表
            """
            # 检查目录是否存在
            if not os.path.exists(json_dir):
                print(f"错误: 目录不存在: {json_dir}")
                return []
            
            # 获取目录中的所有JSON文件
            json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
            
            if not json_files:
                print(f"警告: 在目录 {json_dir} 中未找到JSON文件")
                return []
            
            print(f"找到 {len(json_files)} 个JSON文件，开始批量转换...")
            
            all_output_paths = []
            
            # 处理每个JSON文件
            for json_file in json_files:
                json_path = os.path.join(json_dir, json_file)
                print(f"\n处理文件: {json_file}")
                
                # 更新文件路径
                self.json_file_path = json_path
                
                # 尝试转换
                try:
                    output_paths = self.isat_to_png()
                    if output_paths and isinstance(output_paths, list):
                        all_output_paths.extend(output_paths)
                except Exception as e:
                    print(f"转换文件 {json_file} 时出错: {e}")
            
            print(f"\n批量转换完成，共处理 {len(json_files)} 个文件，生成 {len(all_output_paths)} 个PNG图像")
            return all_output_paths


if __name__ == "__main__":
    
    
    json_file_path = r'E:\LMAI_study\08 diffusion项目\05 AI景观平面图生成\data\josn\final_280.json'

    yaml_data = r'08 diffusion项目\05 AI景观平面图生成\isat.yaml'
    output_dir=r'E:\LMAI_study\08 diffusion项目\05 AI景观平面图生成\data\output'


    converter = ISATConverter(json_file_path = json_file_path,
                             output_dir=output_dir,
                             yaml_path=yaml_data)

    converter.isat_to_png()
    # converter.batch_convert(r'E:\LMAI_study\08 diffusion项目\05 AI景观平面图生成\data\josn')
