# @formatter:on
# coding=utf-8
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import QHeaderView
from PIL import Image
import sys
from process import work_text


# 首页
class Main:
	def __init__(self):
		self.Text = None
		self.Weight = None
		self.ui = QUiLoader().load('resources/Main.ui')
		with open('resources/Main.qss', 'r') as f:
			self.ui.setStyleSheet(f.read())
		# 从resources/Main.ui文件里加载首页样式
		# 绑定首页的两个按钮
		self.ui.ButtonText.setToolTip("对文字智能生成词云")
		self.ui.ButtonWeight.setToolTip("自定义每个词及其权重以生成词云")
		self.ui.ButtonText.clicked.connect(self.TurnToText)
		self.ui.ButtonWeight.clicked.connect(self.TurnToWeight)

	# 转到文本模式
	def TurnToText(self):
		self.Text = Text()
		self.Text.ui.show()
		# 打开新页面后关闭主页
		self.ui.close()

	# 转到权重模式
	def TurnToWeight(self):
		self.Weight = Weight()
		self.Weight.ui.show()
		# 打开新页面后关闭主页
		self.ui.close()


# 文本模式页面
class Text:
	# 两个要用的内部变量
	file_name = ""
	file_type = ""
	# 生成词云图的文本信息和长款像素
	st = ""
	length = 0
	width = 0

	def __init__(self):
		self.Main = None
		self.ui = QUiLoader().load('resources/Text.ui')
		with open('resources/Text.qss', 'r') as f:
			self.ui.setStyleSheet(f.read())
		# 从resources/Test.ui文件里加载首页样式
		# 绑定文本模式的三个按钮：处理、选择文件和返回
		self.ui.ButtonBegin.clicked.connect(self.work)
		self.ui.ButtonChoose.clicked.connect(self.findfile)
		self.ui.ButtonBack.clicked.connect(self.back)

	# 返回首页
	def back(self):
		self.Main = Main()
		self.Main.ui.show()
		# 打开新页面后关闭主页
		self.ui.close()

	# 选择文件函数
	def findfile(self):
		self.file_name, self.file_type = \
			QFileDialog.getOpenFileName(None, '选择文件', '', '文本文件(*.txt)')
		# 从txt文件里导入词云文本信息
		# print(file_type)
		# 显示导入文件的信息以便确认
		self.ui.labelFile.setText(self.file_name)

	# 获取参数
	def getcontent(self):
		# 从文本框获取文本
		self.st = self.ui.TextInput.toPlainText()
		# print(st)
		# print(self.file_name)
		# 从打开的txt文件里获取文本
		if self.file_name != "":
			with open(self.file_name, 'r', encoding='utf-8') as f:  # 打开文件
				self.st += f.read()  # 读取文件
			f.close()
		# 获取词云图长宽
		self.length = self.ui.spinBoxL.value()
		self.width = self.ui.spinBoxW.value()

	def work(self):
		# 先获取需要的参数
		self.getcontent()
		# 防止意外先禁用掉开始按钮
		self.ui.ButtonBegin.setEnabled(False)
		# 生成词云
		message = work_text(self.st, self.length, self.width)
		print(message)
		print(type(message))
		# 根据返回值弹出对应的提示
		if message[0] == 1:
			choice = QMessageBox.question(self.ui, '提示', '生成成功，词云图已保存在output文件夹下，是否查看？')
			if choice == QMessageBox.Yes:
				# 使用系统默认方式打开生成的词云图
				img = Image.open('output/' + message[1] + '.png')
				img.show()
		else:
			# 如果失败就弹出一个有错误提示的提醒框
			QMessageBox.information(self.ui, '提示', "生成失败，错误信息为" + message[1])
		# 恢复关闭的开始按钮
		self.ui.ButtonBegin.setEnabled(True)


class Weight:
	# 以下分别扫文本，词云图长款和{短语-权重}的组数
	st = ""
	length = 0
	width = 0
	linenumber = 0

	def __init__(self):
		self.Main = None
		self.ui = QUiLoader().load('resources/Weight.ui')
		with open('resources/Weight.qss', 'r') as f:
			self.ui.setStyleSheet(f.read())
		# 从resources/Weight.ui文件导入样式
		# 绑定按钮
		self.ui.ButtonBegin.clicked.connect(self.work)
		self.ui.ButtonBack.clicked.connect(self.back)
		self.ui.ButtonNew.clicked.connect(self.newline)
		# 让表格填充区域不留空
		self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		# 设置标题栏的分隔线
		self.ui.tableWidget.horizontalHeader().setStyleSheet(
			"QHeaderView::section{"
			"border-top: 0px solid #E5E5E5;"
			"border-left: 0px solid #E5E5E5;"
			"border-right: 0.5px solid #E5E5E5;"
			"border-bottom: 0.5px solid #E5E5E5;"
			"background-color:white;"
			"padding:4px;"
			"}"
		)

	# 返回首页
	def back(self):
		self.Main = Main()
		self.Main.ui.show()
		self.ui.close()

	# 给表格新增一行，注意下标从0开始
	def newline(self):
		self.ui.tableWidget.insertRow(self.linenumber)
		self.linenumber += 1

	# 获取内容函数
	def getcontent(self):
		# 从表格获取目标词和权重
		for i in range(self.linenumber):
			tep1 = self.ui.tableWidget.item(i, 0).text() + '\n'
			# print(tep1)
			tep2 = self.ui.tableWidget.item(i, 1).text()
			# print(tep2)
			self.st += tep1 * (int(tep2) - int('0'))
		# print(self.st)
		# 获取长宽
		self.length = self.ui.spinBoxL.value()
		self.width = self.ui.spinBoxW.value()

	def work(self):
		# 先获取需要的参数
		self.getcontent()
		# 防止意外先禁用掉开始按钮
		self.ui.ButtonBegin.setEnabled(False)
		# 生成词云
		message = work_text(self.st, self.length, self.width)
		# 根据返回值弹出对应的提示
		if message[0] == 1:
			choice = QMessageBox.question(self.ui, '提示', '生成成功，词云图已保存在output文件夹下，是否查看？')
			if choice == QMessageBox.Yes:
				# 使用系统默认方式打开生成的词云图
				img = Image.open('output/' + message[1] + '.png')
				img.show()
		else:
			# 如果失败就弹出一个有错误提示的提醒框
			QMessageBox.information(self.ui, '提示', "生成失败，错误信息为" + message[1])
		# 恢复关闭的开始按钮
		self.ui.ButtonBegin.setEnabled(True)


# 以下是主函数
app = QApplication(sys.argv)
# 设置程序左上角显示的图标
app.setWindowIcon(QIcon('resources/logo.jpg'))
free = Main()
free.ui.show()
app.exec_()
