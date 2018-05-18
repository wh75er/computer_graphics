import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QImage, QPixmap, QRgba64
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QTableWidgetItem
from math import sqrt, pi, cos, sin


black = Qt.black
white = Qt.white


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("design.ui", self)
        self.setMouseTracking(True)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 520, 520)
        self.canvas.setScene(self.scene)
        self.image = QImage(520, 520, QImage.Format_ARGB32_Premultiplied)
        self.pen = QPen(black)

        self.edges = []
        self.lock = None
        self.prev = None
        self.lazy_draw.setChecked(False)

        self.connect_button.clicked.connect(lambda: self.lock_on_click_button(self))
        self.add_point_button.clicked.connect(lambda: self.add_point_on_click_button(self))
        self.clean_button.clicked.connect(lambda: self.clean_on_click_button(self))
        self.draw_button.clicked.connect(lambda: self.draw_on_click_button(self))

        self.scene.installEventFilter(self)
  



    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            point = event.scenePos()
            self.add_point_mouse(event.scenePos())

        return False

    def add_point_mouse(self, point):
        if self.lock == None:
            self.lock = point
            self.prev = point
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            self.table.insertRow(self.table.rowCount())
            i = self.table.rowCount() - 1
            self.table.setItem(i, 0, item_x)
            self.table.setItem(i, 1, item_y)
            return
        print(point.x(), point.y())
        item_x = QTableWidgetItem("{0}".format(point.x()))
        item_y = QTableWidgetItem("{0}".format(point.y()))
        self.table.insertRow(self.table.rowCount())
        i = self.table.rowCount() - 1
        self.table.setItem(i, 0, item_x)
        self.table.setItem(i, 1, item_y)
        self.edges.append([self.prev.x(), self.prev.y(), 
                        point.x(), point.y()])
        self.scene.addLine(point.x(), point.y(), self.prev.x(), self.prev.y(), self.pen)

        self.prev = point
        print(self.edges)


    def lock_on_click_button(self, win):
        i = len(self.edges)
        if i > 1 and self.lock != self.prev:
            print("ok", self.lock, self.prev)
            self.edges.append([self.prev.x(), self.prev.y(), self.lock.x(), self.lock.y()])
            self.scene.addLine(self.prev.x(), self.prev.y(), self.lock.x(), self.lock.y())
            self.lock = None
            self.prev = None

    def add_point_on_click_button(self, win):
        x = win.x_box.value()
        y = win.y_box.value()
        p = QPoint()
        p.setX(x)
        p.setY(y)
        self.add_point_mouse(p)

    def clean_on_click_button(self, win):
        self.scene.clear()
        self.table.clear()
        self.lock = None
        self.table.setRowCount(0)
        self.edges = []
        self.image.fill(white)

    def get_line_value(self, edge):
        point1 = [edge[0], edge[1]]
        point2 = [edge[2], edge[3]]

        dy = point2[1] - point1[1]
        dx = point2[0] - point1[0]

        left_border = point2[0]
        right_border = point1[0]
        start_y = point2[1]

        if min(point1[0], point2[0]) == point1[0]:
            left_border = point1[0]
            right_border= point2[0]
            start_y = point1[1]

        if not dx:
            return 0, 0, 0, 0

        tg = dy/dx

        print(left_border, right_border, start_y, tg)
        
        return left_border, right_border, start_y, tg

    def set_pipeline(self, edges):
        min_x = edges[0][0]
        max_x = edges[0][0]
        pipe = min_x

        for i in edges:
            if i[0] < min_x:
                min_x = i[0]
            if i[2] < min_x:
                min_x = i[2]
            if i[0] > max_x:
                max_x = i[0]
            if i[2] > max_x:
                max_x = i[2]

        mid = min_x + (max_x - min_x)//2
        l = mid - min_x

        for i in edges:
            if abs(mid - i[0]) < l:
                l = abs(mid - i[0])
                pipe = i[0]
            if abs(mid - i[2]) < l:
                l = abs(mid - i[2])
                pipe = i[2]

        return pipe

    def draw_on_click_button(self, win):
        if not self.edges:
            return

        pix = QPixmap()
        p = QPainter()
        p.begin(win.image)
        p.setPen(QPen(black))

        self.scene.clear()
        pipe = self.set_pipeline(self.edges)
        self.scene.addLine(pipe, 0, pipe, 520)

        for i in self.edges:
            lb, rb, sy, tg = self.get_line_value(i)
            for j in range(int(lb), int(rb+1)):
                p.drawPoint(j, sy)
                print(j, sy)
                sy += tg

        pix.convertFromImage(win.image)
        win.scene.addPixmap(pix)
        p.end()
        




       

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
