from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox
from generate import work_text
from PIL import Image


# 首页
class Main:
	def __init__(self):
		self.Text = None
		self.Weight = None
		self.ui = QUiLoader().load('resources/Main.ui')
		self.ui.ButtonText.clicked.connect(self.TurnToText)
		self.ui.ButtonWeight.clicked.connect(self.TurnToWeight)

	# 转到文本模式
	def TurnToText(self):
		self.Text = Text()
		self.Text.ui.show()
		self.ui.close()

	# 转到权重模式
	def TurnToWeight(self):
		self.Weight = Weight()
		self.Weight.ui.show()
		self.ui.close()


# 文本模式页面
class Text:
	# 两个要用的内部变量
	file_name = ""
	file_type = ""

	def __init__(self):
		self.Main = None
		self.ui = QUiLoader().load('resources/Text.ui')
		self.ui.ButtonBegin.clicked.connect(self.work)
		self.ui.ButtonChoose.clicked.connect(self.findfile)
		self.ui.ButtonBack.clicked.connect(self.back)

	# 返回首页
	def back(self):
		self.Main = Main()
		self.Main.ui.show()
		self.ui.close()

	# 选择文件函数
	def findfile(self):
		self.file_name, self.file_type = QFileDialog.getOpenFileName(None, '选择文件', '', '文本文件(*.txt)')
		# print(file_type)
		self.ui.labelFile.setText(self.file_name)

	# 处理函数
	def work(self):
		st = self.ui.TextInput.toPlainText()
		# print(st)
		# print(self.file_name)
		if self.file_name != "":
			with open(self.file_name, 'r', encoding='utf-8') as f:  # 打开文件
				st += f.read()  # 读取文件
			f.close()
		# 获取长宽
		length = self.ui.spinBoxL.value()
		width = self.ui.spinBoxW.value()
		# 防止以外先禁用掉开始按钮
		self.ui.ButtonBegin.setEnabled(False)
		# 生成词云
		message = work_text(st, length, width)

		if message == "生成成功":
			choice = QMessageBox.question(self.ui, '提示', '词云图已保存在output文件夹下，是否查看？')
			if choice == QMessageBox.Yes:
				img = Image.open("output/wordcloud.png")
				img.show()
		else:
			QMessageBox.information(self.ui, '生成失败', "错误信息为" + message)
		# 恢复关闭的按钮
		self.ui.ButtonBegin.setEnabled(True)


class Weight:
	def __init__(self):
		self.ui = QUiLoader().load('resources/Weight.ui')


# 主函数
app = QApplication([])
app.setWindowIcon(QIcon('resources/logo.jpg'))
free = Main()
free.ui.show()
app.exec_()
