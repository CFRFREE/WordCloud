# @formatter:on
# coding=utf-8
from os import listdir

from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import QHeaderView
from PIL import Image
import sys
import process

content = ""
FromWhere = ""


# 首页
class Main:
	def __init__(self):
		global content
		content = ""
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
	def __init__(self):
		self.Main = None
		self.ui = QUiLoader().load('resources/Text.ui')
		with open('resources/Text.qss', 'r') as f:
			self.ui.setStyleSheet(f.read())
		f.close()
		self.length = 400
		self.width = 400
		self.file_name = ""
		self.file_type = ""
		# 从resources/Test.ui文件里加载首页样式
		# 绑定文本模式的三个按钮：处理、选择文件和返回
		self.ui.ButtonBegin.clicked.connect(self.Begin)
		self.ui.ButtonChoose.clicked.connect(self.Findfile)
		self.ui.ButtonBack.clicked.connect(self.Back)
		self.ui.ButtonToAdvanced.clicked.connect(self.ToAdvanced)

	# 返回首页
	def Back(self):
		self.Main = Main()
		self.Main.ui.show()
		# 打开新页面后关闭主页
		self.ui.close()

	def ToAdvanced(self):
		global FromWhere
		FromWhere = "Text"
		self.Main = Advanced()
		self.Main.ui.show()
		self.ui.close()

	# 选择文件函数
	def Findfile(self):
		self.file_name, self.file_type = \
			QFileDialog.getOpenFileName(None, '选择文件', '', '文本文件(*.txt)')
		# 从txt文件里导入词云文本信息
		# print(file_type)
		# 显示导入文件的信息以便确认
		self.ui.labelFile.setText(self.file_name)

	# 获取参数
	def Getcontent(self):
		# 从文本框获取文本
		global content
		content = self.ui.TextInput.toPlainText()
		# print(st)
		# print(self.file_name)
		# 从打开的txt文件里获取文本
		if self.file_name != "":
			with open(self.file_name, 'r', encoding='utf-8') as f:  # 打开文件
				content += f.read()  # 读取文件
			f.close()
		# 获取词云图长宽
		self.length = self.ui.spinBoxL.value()
		self.width = self.ui.spinBoxW.value()

	def Begin(self):
		# 先获取需要的参数
		self.Getcontent()
		# 防止意外先禁用掉开始按钮
		self.ui.ButtonBegin.setEnabled(False)
		# 生成词云
		global content
		message = process.work_text(content, self.length, self.width)
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
	def __init__(self):
		self.Main = None
		self.ui = QUiLoader().load('resources/Weight.ui')
		with open('resources/Weight.qss', 'r') as f:
			self.ui.setStyleSheet(f.read())
		f.close()
		# 从resources/Weight.ui文件导入样式
		# 绑定按钮
		self.length = 400
		self.width = 400
		self.line = 0
		self.ui.ButtonBegin.clicked.connect(self.Begin)
		self.ui.ButtonBack.clicked.connect(self.Back)
		self.ui.ButtonNew.clicked.connect(self.Newline)
		self.ui.ButtonToAdvanced.clicked.connect(self.ToAdvanced)
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
	def Back(self):
		self.Main = Main()
		self.Main.ui.show()
		self.ui.close()

	def ToAdvanced(self):
		global FromWhere
		FromWhere = "Weight"
		self.Main = Advanced()
		self.Main.ui.show()
		self.ui.close()

	# 给表格新增一行，注意下标从0开始
	def Newline(self):
		self.ui.tableWidget.insertRow(self.line)
		self.line += 1

	# 获取内容函数
	def Getcontent(self):
		# 从表格获取目标词和权重
		global content
		for i in range(self.line):
			tep1 = self.ui.tableWidget.item(i, 0).text() + '\n'
			# print(tep1)
			tep2 = self.ui.tableWidget.item(i, 1).text()
			# print(tep2)
			content += tep1 * (int(tep2) - int('0'))
		# print(self.st)
		# 获取长宽
		if self.ui.spinBoxL.value() != 0:
			self.length = self.ui.spinBoxL.value()
		if self.ui.spinBoxW.value() != 0:
			self.width = self.ui.spinBoxW.value()

	def Begin(self):
		# 先获取需要的参数
		self.Getcontent()
		# 防止意外先禁用掉开始按钮
		self.ui.ButtonBegin.setEnabled(False)
		# 生成词云
		global content
		message = process.work_text(content, self.length, self.width)
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


class Advanced:
	def __init__(self):
		self.Main = None

		# 配置默认参数
		# 词云图长度
		self.length = 400
		# 词云图宽度
		self.width = 400
		# 词云图最小字号
		self.min = 4
		# 词云图最大字号
		self.max = None
		# 词云图字号步进间距
		self.step = 1
		# 水平排版概率
		self.freq = 0.9
		# 字体与字号关联程度
		self.rele = 0.5
		# 字体
		self.font = "simsun"
		# 背景颜色
		self.background = "white"
		# 文字颜色
		self.colour = 'tab10'

		# 从resources/Advanced.ui里加载Advanced页面的样式文件
		self.ui = QUiLoader().load('resources/Advanced.ui')
		with open('resources/Advanced.qss', 'r') as f:
			self.ui.setStyleSheet(f.read())
		f.close()

		# 绑定绘制和返回两个按钮
		self.ui.ButtonBegin.clicked.connect(self.Begin)
		self.ui.ButtonBack.clicked.connect(self.Back)

		# 进行字体下拉框配置
		# 存放C:\Windows\Fonts下所有ttc字体文件
		self.fontlist = []
		path = r'C:\Windows\Fonts'
		f_list = listdir(path)
		for name in f_list:
			if name.split(".")[-1] == 'ttc':
				self.fontlist.append(name.split('.')[0])
		self.ui.comboBoxFont.addItems(self.fontlist)

		# 进行背景颜色下拉框配置
		self.backgroundlist = ["White", "Black", "Blue", "Yellow", "Red", "Green"]
		self.ui.comboBoxBackground.addItems(self.backgroundlist)

		# 进行文字配色下拉框配置
		self.colourlist = ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
		                   'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
		                   'tab20c']
		self.ui.comboBoxColour.addItems(self.colourlist)

	def Back(self):
		# FromWhere存放从哪里进入的Advanced页面
		global FromWhere
		# print(FromWhere)
		if FromWhere == "Text":
			self.Main = Text()
			self.Main.ui.show()
			self.ui.close()
		elif FromWhere == "Weight":
			self.Main = Weight()
			self.Main.ui.show()
			self.ui.close()
		else:
			self.Main = Main()
			self.Main.ui.show()
			self.ui.close()

	def GetParameter(self):
		# 获取所有用户设置的参数并且确保合法
		if self.ui.spinBoxL.value() != 0:
			self.length = self.ui.spinBoxL.value()

		if self.ui.spinBoxW.value() != 0:
			self.width = self.ui.spinBoxW.value()

		if self.ui.comboBoxFont.currentText() in self.fontlist:
			self.font = self.ui.comboBoxFont.currentText()

		if self.ui.comboBoxBackground.currentText() in self.backgroundlist:
			self.background = self.ui.comboBoxBackground.currentText()

		if self.ui.comboBoxColour.currentText() in self.colourlist:
			self.colour = self.ui.comboBoxColour.currentText()

		if self.ui.spinBoxMin.value() != 0:
			self.min = self.ui.spinBoxMin.value()

		if self.ui.spinBoxMax.value() != 0:
			self.max = self.ui.spinBoxMax.value()

		if self.ui.spinBoxStep.value() != 0:
			self.step = self.ui.spinBoxStep.value()

		if self.ui.spinBoxFreq.value() != 0:
			self.freq = self.ui.spinBoxFreq.value()

		if self.ui.spinBoxRele.value() != 0:
			self.rele = self.ui.spinBoxRele.value()

	def Begin(self):
		# 防止意外先禁用掉开始按钮
		self.ui.ButtonBegin.setEnabled(False)
		self.GetParameter()
		# 所有参数的列表
		ParameterList = [self.length, self.width, self.font, self.background, self.max, self.min, self.step,
		                 self.colour, self.freq, self.rele]
		# 生成词云
		global content
		message = process.work_text_advanced(content, ParameterList)
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
