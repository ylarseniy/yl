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
        self.editTable = EditWindow(self)
        self.editTable.show()

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


class EditWindow(QMainWindow):
    def __init__(self, parent=None):
        super(EditWindow, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.updateTable)
        self.Coffee = parent

    def updateTable(self):
        data = []
        for name, element in self.__dict__.items():
            if 'lineEdit' in name:
                data.append(element.text())
        if all(data[1:4] + data[5:]):
            if data[3].lower() in ['true', 'false'] and data[5].isdigit() and data[6].isdigit():
                self.cur = self.Coffee.con.cursor()
                result = self.cur.execute("""SELECT id FROM data""").fetchall()
                if data[0].isdigit() and (int(data[0]),) in result:
                    self.cur.execute(F"""UPDATE data
                        SET species = '{data[1]}', roast = '{data[2]}', grind = '{data[3].lower()}',
                           description = '{data[4]}', price = {data[5]}, volume = {data[6]}
                        WHERE id = {int(data[0])};""")
                else:
                    queue = F"""INSERT INTO data(species, roast, grind, description, price, volume)
                                VALUES('{data[1]}', '{data[2]}', '{data[3]}',
                                       '{data[4]}', {data[5]}, {data[6]})"""
                    self.cur.execute(queue)
                self.Coffee.loadTable()
                self.Coffee.con.commit()
                self.cur.close()


def excepthook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)


if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
