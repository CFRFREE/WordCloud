import os
import sys
from PySide2.QtWidgets import QGridLayout, QApplication, QDialog, QLineEdit, QPushButton, QFileDialog
class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        grid = QGridLayout()
        # 第一行, 打开文件
        self.qlineEdit_selectfile = QLineEdit('文件路径')
        self.qpush_selectfile = QPushButton('选择文件')
        grid.addWidget(self.qlineEdit_selectfile, 0, 1)
        grid.addWidget(self.qpush_selectfile, 0, 2)
        # 第二行, 打开文件夹
        self.qlineEdit_selectfolder = QLineEdit('文件夹路径')
        self.qpush_selectfolder = QPushButton('选择文件夹')
        grid.addWidget(self.qlineEdit_selectfolder, 1, 1)
        grid.addWidget(self.qpush_selectfolder, 1, 2)
        # 第三行, 按钮, 打开文件
        self.qpush_openfile = QPushButton('打开文件')
        grid.addWidget(self.qpush_openfile, 2, 2)
        self.setLayout(grid)
        # 绑定按钮
        self.qpush_selectfile.clicked.connect(self.select_file)
        self.qpush_selectfolder.clicked.connect(self.select_folder)
        self.qpush_openfile.clicked.connect(self.open_file)
    def select_file(self):
        """选择文件
        """
        filename, _ = QFileDialog.getOpenFileName(self, "getOpenFileName",
                                                         './',  # 文件的起始路径
                                                         "All Files (*);;JSON Files (*.json)") # 设置文件类型
        self.qlineEdit_selectfile.setText(filename)
    def select_folder(self):
        """选择文件夹
        """
        foldername = QFileDialog.getExistingDirectory(self, "Select Directory", "./")
        self.qlineEdit_selectfolder.setText(foldername)
    def open_file(self):
        """使用系统的应用打开
        """
        os.startfile(self.qlineEdit_selectfile.text())
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())