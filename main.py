from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog
from generate import work_text


class Main:
	def __init__(self):
		self.Text = None
		self.Weight = None
		self.ui = QUiLoader().load('resources/Main.ui')
		self.ui.ButtonText.clicked.connect(self.TurnToText)
		self.ui.ButtonWeight.clicked.connect(self.TurnToWeight)

	def TurnToText(self):
		self.Text = Text()
		self.Text.ui.show()
		self.ui.close()

	def TurnToWeight(self):
		self.Weight = Weight()
		self.Weight.ui.show()
		self.ui.close()


class Text:
	file_name = ""
	file_type = ""

	def __init__(self):
		self.ui = QUiLoader().load('resources/Text.ui')
		self.ui.ButtonBegin.clicked.connect(self.work)
		self.ui.ButtonChoose.clicked.connect(self.findfile)

	def findfile(self):
		self.file_name, self.file_type = QFileDialog.getOpenFileName(None, '选择文件', '', '文本文件(*.txt)')
		# print(file_type)
		self.ui.labelFile.setText(self.file_name)

	def work(self):
		st = self.ui.TextInput.toPlainText()
		# print(st)
		# print(self.file_name)
		if self.file_name != "":
			with open(self.file_name, 'r', encoding='utf-8') as f:  # 打开文件
				st += f.read()  # 读取文件
			f.close()

		length = self.ui.spinBoxL.value()
		width = self.ui.spinBoxW.value()
		message = work_text(st, length, width)
		print(message)


class Weight:
	def __init__(self):
		self.ui = QUiLoader().load('resources/Weight.ui')


app = QApplication([])
app.setWindowIcon(QIcon('resources/logo.jpg'))
free = Main()
free.ui.show()
app.exec_()
