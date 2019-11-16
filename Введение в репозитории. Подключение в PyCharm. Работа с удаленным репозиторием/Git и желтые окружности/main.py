from random import randint
import sys
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene


class Ellipses(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.pushButton.clicked.connect(self.draw)
        self.scene_widht = self.graphicsView.width() * 7
        self.scene_height = self.graphicsView.height() * 7
        self.pen = QtGui.QPen(QtGui.QColor('black'))
        self.brush = QtGui.QBrush(QtGui.QColor('yellow'))

    def draw(self):
        self.scene.clear()
        count = self.lineEdit_count.text()
        if count.isdigit():
            for n in range(int(count)):
                x = randint(0, self.scene_widht)
                y = randint(0, self.scene_height)
                d = randint(2, round(self.scene_widht / 2))
                self.scene.addEllipse(x, y, d, d, self.pen, self.brush)
                self.update()


def excepthook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)


if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ex = Ellipses()
    ex.show()
    sys.exit(app.exec())
