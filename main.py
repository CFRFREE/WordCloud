from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader


class Main:
	def __init__(self):
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
	def __init__(self):
		self.ui = QUiLoader().load('resources/Text.ui')


class Weight:
	def __init__(self):
		self.ui = QUiLoader().load('resources/Weight.ui')


app = QApplication([])
app.setWindowIcon(QIcon('resources/logo.jpg'))
free = Main()
free.ui.show()
app.exec_()
