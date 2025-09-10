import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl

class WebViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Web Page Viewer")
        self.setGeometry(100, 100, 1000, 800)

        # 创建 QWidget 作为中央窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建 QVBoxLayout 布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 创建 QWebEngineView 控件并设置网页
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://mooool.com"))  # 设置网页网址

        # 启用 JavaScript
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        # 连接网页加载完成信号
        self.browser.loadFinished.connect(self.on_load_finished)

        layout.addWidget(self.browser)

    def on_load_finished(self):
        """
        确保网页加载完成后，可以进行交互
        """
        print("网页加载完成，可以进行交互！")
        # 在这里，你可以做一些额外的操作，如等待网页完全加载后处理网页内容
        # 也可以通过 QWebEngineView 进行动态交互，例如运行 JavaScript

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = WebViewer()
    viewer.show()
    sys.exit(app.exec_())