import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.loadTable()

    def loadTable(self):
        self.cur = self.con.cursor()
        result = self.cur.execute('SELECT * FROM data').fetchall()
        self.tableWidget.setRowCount(len(result))
        for row in range(len(result)):
            for col in range(len(result[0])):
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, result[row][col])
                self.tableWidget.setItem(row, col, item)
        self.cur.close()

    def closeEvent(self, *args, **kwargs):
        self.con.close()


def excepthook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)


if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
