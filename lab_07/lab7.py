import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QImage, QPixmap, QRgba64
from PyQt5.QtCore import Qt, QPoint,QCoreApplication, QEventLoop, QPoint, QPointF
from PyQt5.QtWidgets import QTableWidgetItem
from math import sqrt, pi, cos, sin


black = Qt.black
blue = Qt.blue
white = Qt.white


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.setMouseTracking(True)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 520, 520)
        self.view.setScene(self.scene)
        self.image = QImage(520, 520, QImage.Format_ARGB32_Premultiplied)
        self.pen = QPen(black)

        self.lines = []
        self.cut = []
        self.mode = None;

        self.click_check = False;
        self.prev_point = None;

        self.clear.clicked.connect(lambda: self.clean_on_click_button(self))
        self.line.clicked.connect(lambda: self.add_line_mode(self))
        self.paint.clicked.connect(lambda: self.paint_on_click_button(self))
        self.cutter.clicked.connect(lambda: self.add_cutter_mode(self))

        self.scene.installEventFilter(self)



#-----------------   click event   ------------------------------------

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            point = event.scenePos()
            if(self.mode == "line_mode"):
                self.add_line(event.scenePos())
            if(self.mode == "cutter_mode"):
                self.add_cutter(event.scenePos())

        return False

    def add_point_mouse(self, point):
        print("coords : ", point.x(), point.y());

    def add_line(self, point):
        print("line coords : ", point.x(), point.y());

        if self.click_check:
            line = []
            line.append(self.prev_point)
            line.append(point)
            if line not in self.lines:
                self.add_row(line)
                self.lines.append(line)
                self.scene.addLine(line[0].x(), line[0].y(), line[1].x(), line[1].y(), self.pen);
        else:
            self.prev_point = point;

        self.click_check = False if self.click_check else True

    def add_cutter(self, point):
        print("cutter coords : ", point.x(), point.y());

        if self.click_check:
            line = []
            line.append(self.prev_point)
            line.append(point)
            if not self.cut:
                self.cut = line
                self.scene.addRect(line[0].x(), line[0].y(), abs(line[1].x() - line[0].x()), abs(line[1].y() - line[0].y()), self.pen);
        else:
            self.prev_point = point;


        self.click_check = False if self.click_check else True


#-----------------   buttons   ------------------------------------


    def add_line_mode(self, win):
        self.mode = None if self.mode != None else "line_mode"
        self.button_mode_set();
        self.click_check = False;

    def add_cutter_mode(self, win):
        self.mode = None if self.mode != None else "cutter_mode"
        self.button_mode_set();
        self.click_check = False;

    def paint_on_click_button(self, win):
        if not self.cut or not self.lines:
            print("Check your input data to continue...")
            return

        self.pen.setColor(blue)
        lines_to_fill = self.make_cut()
        self.pen.setColor(black)

    def clean_on_click_button(self, win):
        self.scene.clear()
        self.table.clear()
        self.lines = []
        self.cut = []
        self.image.fill(white)

        r = self.table.rowCount()
        for i in range(r, -1, -1):
            self.table.removeRow(i)


#-----------------   methods   ------------------------------------


    def button_mode_set(self):
        if self.mode == None:
            self.clear.setEnabled(True)
            self.paint.setEnabled(True)
            self.cutter.setEnabled(True)
            self.line.setEnabled(True)
        if self.mode == "line_mode":
            self.clear.setEnabled(False)
            self.paint.setEnabled(False)
            self.cutter.setEnabled(False)
        if self.mode == "cutter_mode":
            self.clear.setEnabled(False)
            self.paint.setEnabled(False)
            self.line.setEnabled(False)

    def add_row(self, line):
        self.table.insertRow(self.table.rowCount())
        i = self.table.rowCount() - 1
        item_b = QTableWidgetItem("[{0}, {1}]".format(line[0].x(), line[0].y()))
        item_e = QTableWidgetItem("[{0}, {1}]".format(line[1].x(), line[1].y()))
        self.table.setItem(i, 0, item_b)
        self.table.setItem(i, 1, item_e)


    def make_cut(self):
        xl = self.cut[0].x()
        xr = self.cut[1].x()
        ya = self.cut[0].y()
        yb = self.cut[1].y()
        xl, xr = min(xl, xr), max(xl, xr)
        ya, yb = max(ya, yb), min(ya, yb)

        for line in self.lines:
            p1 = line[0]
            p2 = line[1]
            t1, t2 = self.get_codes(p1.x(), p1.y(), p2.x(), p2.y(), xl, xr, ya, yb)
            visible = True
            draw_point1 = None;
            draw_point2 = None;
            i = 0
            m = 10**30
            if(t1|t1 == 0 and t2|t2 == 0):
                draw_point1 = p1
                draw_point2 = p2
            else:
                if t1&t2:
                    visible = False
                else:


                    if(t1|t1 == 0):
                        draw_point1 = p1
                        q = p2

                        draw_point2 = self.find_crossings(p1, p2, q, xl, xr, ya, yb)

                        if not draw_point2:
                            visible = False

                        print("The line visibility is ", visible)


                    elif(t2|t2 == 0):
                        draw_point1 = p2
                        q = p1

                        draw_point2 = self.find_crossings(p1, p2, q, xl, xr, ya, yb)

                        if not draw_point2:
                            visible = False

                        print("The line visibility is ", visible)

                    else:
                        q = p1
                        draw_point1 = self.find_crossings(p1, p2, q, xl, xr, ya, yb)
                        q = p2
                        draw_point2 = self.find_crossings(p1, p2, q, xl, xr, ya, yb)

                        if not draw_point1 or not draw_point2:
                            visible = False

                        print("The line visibility is ", visible)

            if visible:
                self.scene.addLine(draw_point1.x(), draw_point1.y(), draw_point2.x(), draw_point2.y(), self.pen);

            print(line)

    def find_crossings(self, p1, p2, q, xl, xr, ya, yb):
        draw_point2 = None
        if p1.x() != p2.x():
            m = (p2.y()-p1.y())/(p2.x()-p1.x())
            if q.x() < xl:
                y_crossing = m*(xl - q.x())+q.y()
                if y_crossing < ya and y_crossing > yb:
                    draw_point2 = QPointF(xl, y_crossing)
            elif q.x() > xr:
                y_crossing = m*(xr - q.x())+q.y()
                if y_crossing < ya and y_crossing > yb:
                    draw_point2 = QPointF(xr, y_crossing)
            elif m:
                if q.y() > ya:
                    x_crossing = 1/m*(ya - q.y())+q.x()
                    if x_crossing < xr and x_crossing > xl:
                        draw_point2 = QPointF(x_crossing, ya)
                elif q.y() < yb:
                    x_crossing = 1/m*(yb - q.y())+q.x()
                    if x_crossing < xr and x_crossing > xl:
                        draw_point2 = QPointF(x_crossing, yb)

        return draw_point2


    def get_codes(self, x1, y1, x2, y2, xl, xr, ya, yb):
        t1 = self.get_code_for_dot(x1, y1, xl, xr, ya, yb)
        t2 = self.get_code_for_dot(x2, y2, xl, xr, ya, yb)
        return t1, t2

    def get_code_for_dot(self, x, y, xl, xr, ya, yb):
        t = 0
        if x < xl:
            t = t|0b0001
        if x > xr:
            t = t|0b0010
        if y < yb:
            t = t|0b0100
        if y > ya:
            t = t|0b1000
        print(bin(t))

        return t



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
