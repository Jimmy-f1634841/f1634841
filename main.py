import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from design import Ui_MainWindow
import cv2

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 处理 OpenCV 图像并显示在 QLabel 上
        self.process_images()

        # 连接保存按钮动作
        self.ui.actionsave_data.triggered.connect(self.save_image)

    def process_images(self):
        image_path = r'C:\Users\hj213\Desktop\qt\your_image.jpg'  # 使用实际图像路径

        # 读取图像
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Unable to load image at {image_path}")
            return

        # 转换为灰度图像
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 二值化图像
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # 识别轮廓
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_img = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 2)

        # 将灰度图像转换为 QImage 并显示在 label_3
        self.display_image(gray, self.ui.label_3)

        # 将二值图像转换为 QImage 并显示在 label_4
        self.display_image(binary, self.ui.label_4)

        # 将识别的轮廓图像转换为 QImage 并显示在一个新的 QLabel 上
        self.display_image(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB), self.ui.label_4)

        # 将原始图像转换为 QImage 并显示在一个新的 QLabel 上
        self.display_image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), self.ui.label_3)

    def display_image(self, img, label):
        height, width = img.shape[:2]
        bytes_per_line = 3 * width if len(img.shape) == 3 else width
        q_format = QtGui.QImage.Format_RGB888 if len(img.shape) == 3 else QtGui.QImage.Format_Grayscale8
        q_image = QtGui.QImage(img.data, width, height, bytes_per_line, q_format)
        pixmap = QtGui.QPixmap.fromImage(q_image)

        # 等比例缩放图像以适应 QLabel
        label_width = label.width()
        label_height = label.height()
        scaled_pixmap = pixmap.scaled(label_width, label_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        # 创建新的 QPixmap，用于在 QLabel 中靠下对齐
        result_pixmap = QtGui.QPixmap(label.size())
        result_pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(result_pixmap)
        painter.drawPixmap(0, label_height - scaled_pixmap.height(), scaled_pixmap)
        painter.end()

        # 将调整后的 QPixmap 设置到 QLabel
        label.setPixmap(result_pixmap)
        # 设置 QLabel 的对齐方式为靠下
        label.setAlignment(QtCore.Qt.AlignBottom)

    def save_image(self):
        # 获取当前显示的图像
        current_pixmap = self.ui.label_3.pixmap()

        if current_pixmap:
            # 打开文件保存对话框
            file_dialog = QtWidgets.QFileDialog(self)
            file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
            file_dialog.setDefaultSuffix('jpg')
            file_path, _ = file_dialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.xpm *.jpg)")

            if file_path:
                # 保存当前显示的图像
                current_pixmap.save(file_path)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
