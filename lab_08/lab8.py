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

        self.lines = []
        self.cut = []
        self.mode = None;
        self.lock = None;

        self.line_2.setEnabled(False)

        self.click_check = False;
        self.start_point = None;
        self.prev_point = None;

        self.clean.clicked.connect(lambda: self.clean_on_click_button(self))
        self.line.clicked.connect(lambda: self.add_line_mode(self))
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

        if self.click_check:
            self.lock = None;
            line = []
            line.append(self.prev_point)
            line.append(point)
            if line not in self.lines:
                self.pen.setColor(blue)
                self.add_row(line, self.table_lines)
                self.lines.append(line)
                self.scene.addLine(line[0].x(), line[0].y(), line[1].x(), line[1].y(), self.pen);
                self.pen.setColor(black)
        else:
            self.prev_point = point;

        self.click_check = False if self.click_check else True

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

    def paint_on_click_button(self, win):
        if not self.cut or not self.lines:
            print("Check your input data to continue...")
            return

        self.pen.setColor(red)
        self.make_cut()
        self.pen.setColor(blue)

    def clean_on_click_button(self, win):
        self.line_2.setEnabled(False)
        self.scene.clear()
        self.lines = []
        self.cut = []
        self.image.fill(white)
        self.pen.setColor(black)
        self.table_clean(self.table_cut)
        self.table_clean(self.table_lines)

    def add_par_line(self, win):
        if not self.cut:
            return;

        self.pen.setColor(blue)

        point1 = QPoint(self.cut[0][0].x() - 10, self.cut[0][0].y() - 10)
        point2 = QPoint(self.cut[0][1].x() - 10, self.cut[0][1].y() - 10)
        line = [point1, point2]
        if line not in self.lines:
            self.add_row(line, self.table_lines)
            self.lines.append(line)
            self.scene.addLine(line[0].x(), line[0].y(), line[1].x(), line[1].y(), self.pen);

        point1 = QPoint(self.cut[0][0].x() + 10, self.cut[0][0].y() + 10)
        point2 = QPoint(self.cut[0][1].x() + 10, self.cut[0][1].y() + 10)
        line = [point1, point2]
        if line not in self.lines:
            self.add_row(line, self.table_lines)
            self.lines.append(line)
            self.scene.addLine(line[0].x(), line[0].y(), line[1].x(), line[1].y(), self.pen);

        self.pen.setColor(black)


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
            return sign
        return False

    def param_line(self, p1, p2, t):
        return QPointF(p1.x()+(p2.x() - p1.x())*t, p1.y()+(p2.y()-p1.y())*t)

    def sign(self, a):
        if a <= 0:
            return False;
        return True;

    def normal(self, vec, norm):
        if norm < 0:
            return QPointF(vec.y(), -1*vec.x())
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
            self.line.setEnabled(True)
        if self.mode == "line_mode":
            self.clean.setEnabled(False)
            self.paint.setEnabled(False)
            self.cutter.setEnabled(False)
            self.line_2.setEnabled(False)
        if self.mode == "cutter_mode":
            self.clean.setEnabled(False)
            self.paint.setEnabled(False)
            self.line.setEnabled(False)
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
        norm = self.checkConvexPolygon()
        if(norm == False):
            print("The polygon is not convex! Try another one...")
            return;
        for i in self.lines:
            dp1, dp2 = self.cyrus_beck(i, self.cut, norm)
            if dp1 and dp2:
                self.pen.setColor(red)
                self.scene.addLine(dp1.x(), dp1.y(), dp2.x(), dp2.y(), self.pen)
                self.pen.setColor(black)

    def cyrus_beck(self, line, edges, norm):
        draw_point1 = None
        draw_point2 = None
        p1 = line[0]
        p2 = line[1]
        d = p2-p1
        tb = 0
        ta = 1
        for edge in edges:
            n = self.normal(self.vec(edge[0], edge[1]), norm)
            w = p1 - edge[0]
            w_scalar = self.scalar(w, n)
            d_scalar = self.scalar(d, n)
            if d_scalar:
                t = -(w_scalar/d_scalar)
                if d_scalar > 0:
                    if t<=1:
                        tb = max(t, tb)
                    else:
                        return draw_point1, draw_point2
                if d_scalar < 0:
                    if t>=0:
                        ta = min(t, ta)
                    else:
                        return draw_point1, draw_point2
            else:
                if w_scalar < 0:
                    return draw_point1, draw_point2;
                elif w_scalar > 0:
                    break;

        if tb < ta:
            draw_point1 = self.param_line(p1, p2, tb)
            draw_point2 = self.param_line(p1, p2, ta)

        return draw_point1, draw_point2





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
