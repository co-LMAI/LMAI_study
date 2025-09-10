from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QFileDialog, \
    QLabel, QComboBox, QSpinBox, QCheckBox, QGroupBox, QRadioButton, QFormLayout, QStackedWidget, QWidget, QDoubleSpinBox
from PyQt5.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("景观设计AI工具")  # 设置窗口标题
        self.setGeometry(100, 100, 1000, 800)  # 设置窗口大小

        # 创建 QStackedWidget 控件，作为主要的页面容器，用于切换不同页面
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # 看板主页面（包含功能卡片）
        self.kanban_page = QWidget()
        self.kanban_layout = QVBoxLayout()  # 看板页面布局
        self.kanban_page.setLayout(self.kanban_layout)
        self.stack.addWidget(self.kanban_page)  # 将看板页面添加到 QStackedWidget 中

        # 初始化看板视图（添加功能卡片）
        self.init_kanban_view()

    def init_kanban_view(self):
        """
        初始化看板视图，添加多个功能模块卡片
        """
        # 创建看板视图的三个模块卡片，点击后进入不同的页面
        self.create_kanban_card("🌧️ 雨水径流分析", self.init_rainfall_tab)
        self.create_kanban_card("👁️ 三维视域分析", self.init_viewshed_tab)
        self.create_kanban_card("🎨 概念方案生成", self.init_concept_tab)
        self.create_kanban_card("⚙️ 系统设置", self.init_system_tab)

    def create_kanban_card(self, title, target_widget_creator):
        """
        创建一个卡片按钮，并设置点击事件来跳转到目标页面
        """
        card_button = QPushButton(title)
        card_button.setFixedSize(200, 100)  # 设置卡片按钮大小
        card_button.clicked.connect(lambda: self.show_module_page(target_widget_creator))  # 点击时跳转
        self.kanban_layout.addWidget(card_button)  # 将卡片添加到看板布局中

    def show_module_page(self, create_func):
        """
        显示对应的功能页面
        """
        module_widget = create_func()  # 创建对应功能页面的 QWidget
        self.stack.addWidget(module_widget)  # 将页面添加到 QStackedWidget
        self.stack.setCurrentWidget(module_widget)  # 切换到该页面

    # 各个模块页面（每个功能页面）

    def init_rainfall_tab(self):
        """
        雨水径流分析功能页面
        """
        rainfall_tab = QWidget()
        layout = QVBoxLayout()

        # 返回按钮
        back_button = QPushButton("返回")
        back_button.clicked.connect(self.return_to_kanban)  # 返回到看板页面
        layout.addWidget(back_button)

        dem_label = QLabel("上传 DEM 数据 (.tif/.asc):")
        self.dem_input = QPushButton("选择文件")
        self.dem_input.clicked.connect(self.select_dem_file)  # 选择 DEM 文件

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

        self.simulate_button = QPushButton("开始模拟")
        self.simulate_button.clicked.connect(self.simulate_rainfall)  # 开始模拟
        self.result_label = QLabel("分析结果会显示在这里")

        layout.addWidget(dem_label)
        layout.addWidget(self.dem_input)
        layout.addWidget(params_group)
        layout.addWidget(self.simulate_button)
        layout.addWidget(self.result_label)

        rainfall_tab.setLayout(layout)
        return rainfall_tab

    def init_viewshed_tab(self):
        """
        三维视域分析功能页面
        """
        viewshed_tab = QWidget()
        layout = QVBoxLayout()

        # 返回按钮
        back_button = QPushButton("返回")
        back_button.clicked.connect(self.return_to_kanban)
        layout.addWidget(back_button)

        model_label = QLabel("上传 3D 模型 (.3dm):")
        self.model_input = QPushButton("选择文件")
        self.model_input.clicked.connect(self.select_3d_model)

        viewshed_params_group = QGroupBox("观察点设置")
        viewshed_params_layout = QFormLayout()
        self.viewpoint_height = QDoubleSpinBox()
        self.viewpoint_height.setRange(0.0, 10.0)
        self.viewpoint_height.setValue(1.8)
        viewshed_params_layout.addRow("视点高度 (m):", self.viewpoint_height)

        self.terrain_blocking = QCheckBox("考虑地形遮挡")
        viewshed_params_layout.addRow("地形遮挡:", self.terrain_blocking)

        viewshed_params_group.setLayout(viewshed_params_layout)

        self.calculate_viewshed_button = QPushButton("计算视域")
        self.calculate_viewshed_button.clicked.connect(self.calculate_viewshed)
        self.viewshed_result_label = QLabel("视域分析结果会显示在这里")

        layout.addWidget(model_label)
        layout.addWidget(self.model_input)
        layout.addWidget(viewshed_params_group)
        layout.addWidget(self.calculate_viewshed_button)
        layout.addWidget(self.viewshed_result_label)

        viewshed_tab.setLayout(layout)
        return viewshed_tab

    def init_concept_tab(self):
        """
        概念方案生成功能页面
        """
        concept_tab = QWidget()
        layout = QVBoxLayout()

        # 返回按钮
        back_button = QPushButton("返回")
        back_button.clicked.connect(self.return_to_kanban)
        layout.addWidget(back_button)

        description_label = QLabel("设计需求描述:")
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("例如：现代风格滨水公园，包含木质平台和开花乔木...")

        self.style_group = QGroupBox("出图风格")
        self.style_layout = QVBoxLayout()
        self.realistic_style = QRadioButton("写实风格")
        self.hand_drawn_style = QRadioButton("手绘风格")
        self.analysis_style = QRadioButton("分析图风格")
        self.style_layout.addWidget(self.realistic_style)
        self.style_layout.addWidget(self.hand_drawn_style)
        self.style_layout.addWidget(self.analysis_style)
        self.style_group.setLayout(self.style_layout)

        self.generate_button = QPushButton("生成方案")
        self.generate_button.clicked.connect(self.generate_concept)
        self.concept_result_label = QLabel("生成的设计方案会显示在这里")

        layout.addWidget(description_label)
        layout.addWidget(self.description_input)
        layout.addWidget(self.style_group)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.concept_result_label)

        concept_tab.setLayout(layout)
        return concept_tab

    def init_system_tab(self):
        """
        系统设置功能页面
        """
        system_tab = QWidget()
        layout = QVBoxLayout()

        # 返回按钮
        back_button = QPushButton("返回")
        back_button.clicked.connect(self.return_to_kanban)
        layout.addWidget(back_button)

        self.ai_models_group = QGroupBox("AI模型管理")
        self.ai_models_layout = QFormLayout()
        self.rainfall_model = QComboBox()
        self.rainfall_model.addItems(["SWMM-Urban", "HEC-HMS"])
        self.image_model = QComboBox()
        self.image_model.addItems(["Stable Diffusion", "Midjourney"])
        self.ai_models_layout.addRow("雨水分析模型:", self.rainfall_model)
        self.ai_models_layout.addRow("图像生成模型:", self.image_model)
        self.ai_models_group.setLayout(self.ai_models_layout)

        self.check_updates_button = QPushButton("检查更新")
        self.check_updates_button.clicked.connect(self.check_updates)

        layout.addWidget(self.ai_models_group)
        layout.addWidget(self.check_updates_button)

        system_tab.setLayout(layout)
        return system_tab

    # 事件处理方法（对应每个模块的功能）

    def select_dem_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择 DEM 文件", "", "DEM Files (*.tif *.asc)")
        if file_name:
            self.dem_input.setText(file_name)

    def simulate_rainfall(self):
        self.result_label.setText("模拟完成！结果已生成。")

    def select_3d_model(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择 3D 模型文件", "", "3D Model Files (*.3dm)")
        if file_name:
            self.model_input.setText(file_name)

    def calculate_viewshed(self):
        self.viewshed_result_label.setText("视域计算完成！结果已生成。")

    def generate_concept(self):
        description = self.description_input.text()
        style = "写实风格" if self.realistic_style.isChecked() else "手绘风格" if self.hand_drawn_style.isChecked() else "分析图风格"
        
        self.concept_result_label.setText(f"生成的设计方案：{description} - 风格: {style}")

    def check_updates(self):
        print("检查更新...")

    # 返回到看板页面
    def return_to_kanban(self):
        self.stack.setCurrentWidget(self.kanban_page)


# 启动应用
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())