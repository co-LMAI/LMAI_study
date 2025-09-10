from PyQt5.QtWidgets import QDoubleSpinBox,QWidget,QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QLabel, QComboBox, QSpinBox, QSlider, QCheckBox, QGroupBox, QRadioButton, QGridLayout, QFormLayout, QTabWidget, QFrame
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("景观设计AI工具")
        self.setGeometry(100, 100, 1000, 800)

        # 创建 QTabWidget 控件，作为主要的布局
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 初始化各个模块
        self.init_rainfall_tab()
        self.init_viewshed_tab()
        self.init_concept_tab()
        self.init_system_tab()

    def init_rainfall_tab(self):
        rainfall_tab = QWidget()
        self.tabs.addTab(rainfall_tab, "🌧️ 雨水径流分析")

        layout = QVBoxLayout()
        rainfall_tab.setLayout(layout)

        # 输入 DEM 数据
        dem_label = QLabel("上传DEM数据 (.tif/.asc):")
        self.dem_input = QPushButton("选择文件")
        self.dem_input.clicked.connect(self.select_dem_file)
        
        # 参数设置
        params_group = QGroupBox("分析参数")
        params_layout = QFormLayout()
        self.rain_intensity = QSpinBox()
        self.rain_intensity.setRange(0, 500)
        self.rain_intensity.setValue(50)
        params_layout.addRow("降雨强度 (mm/h):", self.rain_intensity)

        self.soil_type = QComboBox()
        self.soil_type.addItems(["黏土", "砂土", "壤土"])
        params_layout.addRow("土壤类型:", self.soil_type)

        params_group.setLayout(params_layout)

        # 模拟按钮
        self.simulate_button = QPushButton("开始模拟")
        self.simulate_button.clicked.connect(self.simulate_rainfall)

        # 结果展示
        self.result_label = QLabel("分析结果会显示在这里")

        layout.addWidget(dem_label)
        layout.addWidget(self.dem_input)
        layout.addWidget(params_group)
        layout.addWidget(self.simulate_button)
        layout.addWidget(self.result_label)

    def init_viewshed_tab(self):
        viewshed_tab = QWidget()
        self.tabs.addTab(viewshed_tab, "👁️ 三维视域分析")

        layout = QVBoxLayout()
        viewshed_tab.setLayout(layout)

        # 输入 3D 模型
        model_label = QLabel("上传 3D 模型 (.3dm):")
        self.model_input = QPushButton("选择文件")
        self.model_input.clicked.connect(self.select_3d_model)

        # 参数设置
        viewshed_params_group = QGroupBox("观察点设置")
        viewshed_params_layout = QFormLayout()
        self.viewpoint_height = QDoubleSpinBox()
        self.viewpoint_height.setRange(0.0, 10.0)
        self.viewpoint_height.setValue(1.8)
        viewshed_params_layout.addRow("视点高度 (m):", self.viewpoint_height)

        self.terrain_blocking = QCheckBox("考虑地形遮挡")
        viewshed_params_layout.addRow("地形遮挡:", self.terrain_blocking)

        viewshed_params_group.setLayout(viewshed_params_layout)

        # 计算按钮
        self.calculate_viewshed_button = QPushButton("计算视域")
        self.calculate_viewshed_button.clicked.connect(self.calculate_viewshed)

        # 结果展示
        self.viewshed_result_label = QLabel("视域分析结果会显示在这里")

        layout.addWidget(model_label)
        layout.addWidget(self.model_input)
        layout.addWidget(viewshed_params_group)
        layout.addWidget(self.calculate_viewshed_button)
        layout.addWidget(self.viewshed_result_label)

    def init_concept_tab(self):
        concept_tab = QWidget()
        self.tabs.addTab(concept_tab, "🎨 概念方案生成")

        layout = QVBoxLayout()
        concept_tab.setLayout(layout)

        # 输入需求描述
        description_label = QLabel("设计需求描述:")
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("例如：现代风格滨水公园，包含木质平台和开花乔木...")

        # 风格选择
        self.style_group = QGroupBox("出图风格")
        self.style_layout = QVBoxLayout()
        self.realistic_style = QRadioButton("写实风格")
        self.hand_drawn_style = QRadioButton("手绘风格")
        self.analysis_style = QRadioButton("分析图风格")
        self.style_layout.addWidget(self.realistic_style)
        self.style_layout.addWidget(self.hand_drawn_style)
        self.style_layout.addWidget(self.analysis_style)
        self.style_group.setLayout(self.style_layout)

        # 生成方案按钮
        self.generate_button = QPushButton("生成方案")
        self.generate_button.clicked.connect(self.generate_concept)

        # 结果展示
        self.concept_result_label = QLabel("生成的设计方案会显示在这里")

        layout.addWidget(description_label)
        layout.addWidget(self.description_input)
        layout.addWidget(self.style_group)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.concept_result_label)

    def init_system_tab(self):
        system_tab = QWidget()
        self.tabs.addTab(system_tab, "⚙️ 系统设置")

        layout = QVBoxLayout()
        system_tab.setLayout(layout)

        # AI模型管理
        self.ai_models_group = QGroupBox("AI模型管理")
        self.ai_models_layout = QFormLayout()
        self.rainfall_model = QComboBox()
        self.rainfall_model.addItems(["SWMM-Urban", "HEC-HMS"])
        self.image_model = QComboBox()
        self.image_model.addItems(["Stable Diffusion", "Midjourney"])
        self.ai_models_layout.addRow("雨水分析模型:", self.rainfall_model)
        self.ai_models_layout.addRow("图像生成模型:", self.image_model)
        self.ai_models_group.setLayout(self.ai_models_layout)

        # 检查更新按钮
        self.check_updates_button = QPushButton("检查更新")
        self.check_updates_button.clicked.connect(self.check_updates)

        layout.addWidget(self.ai_models_group)
        layout.addWidget(self.check_updates_button)

    # 事件处理方法
    def select_dem_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择 DEM 文件", "", "DEM Files (*.tif *.asc)")
        if file_name:
            self.dem_input.setText(file_name)

    def simulate_rainfall(self):
        # 在这里你可以将实际的模拟功能接入
        self.result_label.setText("模拟完成！结果已生成。")

    def select_3d_model(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择 3D 模型文件", "", "3D Model Files (*.3dm)")
        if file_name:
            self.model_input.setText(file_name)

    def calculate_viewshed(self):
        # 视域分析的计算逻辑
        self.viewshed_result_label.setText("视域计算完成！结果已生成。")

    def generate_concept(self):
        # 概念方案生成逻辑
        description = self.description_input.text()
        style = "写实风格" if self.realistic_style.isChecked() else "手绘风格" if self.hand_drawn_style.isChecked() else "分析图风格"
        self.concept_result_label.setText(f"生成的设计方案：{description} - 风格: {style}")

    def check_updates(self):
        # 检查更新的逻辑
        print("检查更新...")

# 启动应用
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())