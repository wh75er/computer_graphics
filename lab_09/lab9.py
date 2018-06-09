import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QImage, QPixmap, QRgba64
from PyQt5.QtCore import Qt, QPoint,QCoreApplication, QEventLoop, QPoint, QPointF
from PyQt5.QtWidgets import QTableWidgetItem
from math import sqrt, pi, cos, sin


black = Qt.black
blue = Qt.blue
red = Qt.red
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

        self.polygon = []
        self.cut = []
        self.mode = None;
        self.lock = None;

        self.line_2.setEnabled(False)

        self.click_check = False;
        self.start_point = None;
        self.prev_point = None;

        self.clean.clicked.connect(lambda: self.clean_on_click_button(self))
        self._polygon.clicked.connect(lambda: self.add_line_mode(self))
        self.line_2.clicked.connect(lambda: self.add_par_line(self))
        self._lock.clicked.connect(lambda: self.lock_on_click_button(self))
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

        if self.lock:
            line = []
            line.append(self.prev_point)
            line.append(point)
            if line not in self.polygon:
                self.pen.setColor(blue)
                self.add_row(line, self.table_polygon)
                self.polygon.append(line)
                self.scene.addLine(line[0].x(), line[0].y(), line[1].x(), line[1].y(), self.pen);
            self.prev_point = point;
        else:
            self.lock = True;
            self.start_point = point;
            self.prev_point = point;

    def add_cutter(self, point):
        print("cutter coords : ", point.x(), point.y());

        if self.lock:
            line = []
            line.append(self.prev_point)
            line.append(point)
            if line not in self.cut:
                self.add_row(line, self.table_cut)
                self.cut.append(line)
                self.scene.addLine(line[0].x(), line[0].y(), line[1].x(), line[1].y(), self.pen);
            self.prev_point = point;
        else:
            self.lock = True;
            self.start_point = point;
            self.prev_point = point;


#-----------------   buttons   ------------------------------------


    def add_line_mode(self, win):
        self.mode = None if self.mode != None else "line_mode"
        self.button_mode_set();
        self.click_check = False;

    def add_cutter_mode(self, win):
        self.mode = None if self.mode != None else "cutter_mode"
        self.button_mode_set();
        self.click_check = False;

    def lock_on_click_button(self, win):
        print("locked");
        if self.prev_point and self.lock:
            line = []
            line.append(self.prev_point)
            line.append(self.start_point)
            self.add_row(line, self.table_cut)
            self.cut.append(line)
            self.scene.addLine(self.prev_point.x(), self.prev_point.y(),
                                self.start_point.x(), self.start_point.y(), self.pen);
            self.prev_point = None;
            self.start_point = None;
            self.lock = None;
            self.pen.setColor(black)

    def paint_on_click_button(self, win):
        if not self.cut or not self.polygon:
            print("Check your input data to continue...")
            return

        self.pen.setColor(red)
        self.make_cut()
        self.pen.setColor(blue)

    def clean_on_click_button(self, win):
        self.line_2.setEnabled(False)
        self.scene.clear()
        self.polygon = []
        self.cut = []
        self.image.fill(white)
        self.pen.setColor(black)
        self.table_clean(self.table_cut)
        self.table_clean(self.table_polygon)

    def add_par_line(self, win):
        if not self.cut:
            return;

        print("parrallel lines")


#-----------------   methods   ------------------------------------

    def checkConvexPolygon(self):
        line_start = self.cut[0]
        line_end = self.cut[len(self.cut)-1]
        rotate = 1;
        sign = None;
        for i in range(len(self.cut) - 1):
            line_1 = self.cut[i]
            line_2 = self.cut[i+1]
            v1 = self.vec(line_1[0], line_1[1])
            v2 = self.vec(line_2[0], line_2[1])
            rotate = v1.x()*v2.y() - v1.y()*v2.x()
            if sign:
                if self.sign(sign) != self.sign(rotate):
                    sign = None
                    break;
            else:
                sign = rotate
        if sign:
            v1 = self.vec(line_end[0], line_end[1])
            v2 = self.vec(line_start[0], line_start[1])
            rotate = v1.x()*v2.y() - v1.y()*v2.x()	# finding z direction of [a, b]
            if self.sign(sign) != self.sign(rotate):
                sign = None

        if sign:
            return True
        return False

    def param_line(self, p1, p2, t):
        return QPointF(p1.x()+(p2.x() - p1.x())*t, p1.y()+(p2.y()-p1.y())*t)

    def sign(self, a):
        if a <= 0:
            return False;
        return True;

    def normal(self, vec):
        return QPointF(-1*vec.y(), vec.x())

    def vec(self, p1, p2):
        return p2-p1;

    def vecLen(self, vec):
        return  sqrt(vec.x()**2 + vec.y()**2)

    def scalar(self, v1, v2):
        return v1.x()*v2.x() + v1.y()*v2.y()

    def table_clean(self, table):
        table.clear()
        r = table.rowCount()
        for i in range(r, -1, -1):
            table.removeRow(i)

    def button_mode_set(self):
        if self.mode == None:
            if self.cut:
                self.line_2.setEnabled(True)
            self.clean.setEnabled(True)
            self.paint.setEnabled(True)
            self.cutter.setEnabled(True)
            self._polygon.setEnabled(True)
        if self.mode == "line_mode":
            self.clean.setEnabled(False)
            self.paint.setEnabled(False)
            self.cutter.setEnabled(False)
            self.line_2.setEnabled(False)
        if self.mode == "cutter_mode":
            self.clean.setEnabled(False)
            self.paint.setEnabled(False)
            self._polygon.setEnabled(False)
            self.line_2.setEnabled(False)

    def add_row(self, line, table):
        table.insertRow(table.rowCount())
        i = table.rowCount() - 1
        item_b = QTableWidgetItem("[{0}, {1}]".format(line[0].x(), line[0].y()))
        item_e = QTableWidgetItem("[{0}, {1}]".format(line[1].x(), line[1].y()))
        table.setItem(i, 0, item_b)
        table.setItem(i, 1, item_e)


    def make_cut(self):
        print("pain")
        if(not self.checkConvexPolygon()):
            print("The polygon is not convex! Try another one...")
            return

        for i in self.cut:
            edge = i
            cutted = []
            for j in self.polygon:
                line = j
                t = crossing(line, edge)
                if t:
                    cutted.append(t)
            s = line[1]
            if visible(s, edge):
                cutted.append(s)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
