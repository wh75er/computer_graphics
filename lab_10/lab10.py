import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QImage, QPixmap, QRgba64
from PyQt5.QtCore import Qt, QPoint,QCoreApplication, QEventLoop, QPoint, QPointF
from PyQt5.QtWidgets import QTableWidgetItem
from math import sqrt, pi, cos, sin, exp
import copy


black = Qt.black
blue = Qt.blue
red = Qt.red
white = Qt.white
green = Qt.green
darkGreen = Qt.darkGreen

k = 35
shx = 600 / 2
shy = 600 / 2


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.setMouseTracking(True)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 600, 600)
        self.view.setScene(self.scene)
        self.image = QImage(600, 600, QImage.Format_ARGB32_Premultiplied)
        self.pen = QPen(black)

        self.funcs.addItems(["2 * cos(x * z)",
                            "5*sin(x) - cos(z)",
                            "exp(sin(sqrt(x**2 + z**2)))"])

        self.pen.setColor(green)
        self.scene.setBackgroundBrush(black)

        self.x_angle.valueChanged.connect(lambda: self.angle_changed(self))
        self.y_angle.valueChanged.connect(lambda: self.angle_changed(self))
        self.z_angle.valueChanged.connect(lambda: self.angle_changed(self))
        self.draw.clicked.connect(lambda: self.draw_on_click_button(self))

        self.scene.installEventFilter(self)



#-----------------   click event   ------------------------------------

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            point = event.scenePos()
            self.add_point_mouse(point)

        return False

    def add_point_mouse(self, point):
        print("coords : ", point.x(), point.y());


#-----------------   buttons   ------------------------------------

    def draw_on_click_button(self, win):
        print("init")


#-----------------   methods   ------------------------------------

    def f(self, x, z):
        return eval(self.funcs.currentText())

    def angle_changed(self, win):
        self.scene.clear()
        self.floating_horizon()

    def floating_horizon(self):
        top = [0 for x in range(1, int(self.scene.width())+1)]
        bottom = [self.scene.height() for x in range(1, int(self.scene.width())+1)]

        xl, xr = -1, -1
        yl, yr = -1, -1

        zMax = self.max_z.value()
        zMin = self.min_z.value()
        xMax = self.max_x.value()
        xMin = self.min_x.value()
        zStep = self.step_z.value()
        xStep = self.step_x.value()

        z = zMax
        while z>=zMin:
            xPrev = xMin
            yPrev = self.f(xMin, z)
            xPrev, yPrev, zT = self.transform(xPrev, yPrev, z)

            if xl != -1:
                top, bottom = horizon(xl, yl, xPrev, yPrev, top, bottom)
            xl = xPrev
            yl = yPrev

            flagPrev = visible(xPrev, yPrev, top, bottom)

            x = xMin
            while x <= xMax:
                y = self.f(x, z)
                xCurr, yCurr, zT = self.transform(x, y, z)

                flagCurr = visible(xCurr, yCurr, top, bottom)
                if flagCurr == flagPrev:
                    if flagCurr == 1 or flagCurr == -1:
                        self.scene.addLine(xPrev, yPrev, xCurr, yCurr, self.pen)
                        top, bottom = horizon(xPrev, yPrev, xCurr, yCurr, top, bottom)
                else:
                    if flagCurr == 0:
                        if flagPrev == 1:
                            xi, yi = intersection(xPrev, yPrev, xCurr, yCurr, top)
                        else:
                            xi, yi = intersection(xPrev, yPrev, xCurr, yCurr, bottom)
                        self.scene.addLine(xPrev, yPrev, xi, yi, self.pen)
                        top, bottom = horizon(xPrev, yPrev, xi, yi, top, bottom)
                    else:
                        if flagPrev == 0:
                            xi, yi = intersection(xPrev, yPrev, xCurr, yCurr, top)
                            self.scene.addLine(xi, yi, xCurr, yCurr, self.pen)
                            top, bottom = horizon(xi, yi, xCurr, yCurr, top, bottom)
                        else:
                            if flagCurr == 1:
                                xi, yi = intersection(xPrev, yPrev, xCurr, yCurr, bottom)
                            else:
                                xi, yi = intersection(xPrev, yPrev, xCurr, yCurr, top)
                            self.scene.addLine(xPrev, yPrev, xi, yi, self.pen)
                            top, bottom = horizon(xPrev, yPrev, xi, yi, top, bottom)
                            if flagCurr == 1:
                                xi, yi = intersection(xPrev, yPrev, xCurr, yCurr, top)
                            else:
                                xi, yi = intersection(xPrev, yPrev, xCurr, yCurr, bottom)
                            self.scene.addLine(xPrev, yPrev, xi, yi, self.pen)
                            top, bottom = horizon(xi, yi, xCurr, yCurr, top, bottom)
                flagPrev = flagCurr
                xPrev = xCurr
                yPrev = yCurr

                x += xStep

            if z != zMax:
                xr = xMax
                yr = self.f(xr, z-zStep)
                xr, yr, zT = self.transform(xr, yr, z)
                top, bottom = horizon(xr, yr, xPrev, yPrev, top, bottom)

            z -= zStep

    def transform(self, x, y, z):
        x, y, z = rotateX(x, y, z, self.x_angle.value())
        x, y, z = rotateY(x, y, z, self.y_angle.value())
        x, y, z = rotateZ(x, y, z, self.z_angle.value())
        x = x * k + shx
        y = y * k + shy
        return round(x), round(y), round(z)



#-----------------   functions  ------------------------------------\

def horizon(x1, y1, x2, y2, top, bottom):
    if x2 < x1:
        x1, y1, x2, y2 = x2, y2, x1, y1
    if x2-x1 == 0:
        top[x2] = max(top[x2], max(y1, y2))
        bottom[x2] = min(bottom[x2], min(y1, y2))
    else:
        tilt = (y2-y1)/(x2-x1)
        y = y1
        for x in range(round(x1), round(x2+1)):
            y += tilt
            top[x] = max(top[x], y)
            bottom[x] = min(bottom[x], y)

    return top, bottom


def visible(x, y, top, bottom):
    if y < top[x] and y > bottom[x]:
        return 0
    elif y >= top[x] :
        return 1
    else:
        return -1


def sign(a):
    if a < 0:
        return -1
    if a == 0:
        return 0
    if a > 0:
        return 1
    return None

def intersection(x1, y1, x2, y2, arr):
    if x2 < x1:
        x1, y1, x2, y2 = x2, y2, x1, y1
    if x2-x1 == 0:
        xi = x2
        yi = arr[x2]
    else:
        tilt = (y2-y1)/(x2-x1)
        ySign = sign(y1 + tilt - arr[x1+1])
        cSign = ySign
        yi = y1 + tilt
        xi = x1 + 1
        while cSign == ySign and xi <= x2:
            yi += tilt
            xi += 1
            cSign = sign(yi - arr[xi])
        if abs(yi - tilt - arr[xi-1]) <= abs(yi - arr[xi]):
            yi -= tilt
            xi -= 1
    return round(xi), round(yi)




def rotateX(x, y, z, a):
    a = a * pi / 180
    buf = y
    y = cos(a) * y - sin(a) * z
    z = cos(a) * z + sin(a) * buf
    return x, y, z


def rotateY(x, y, z, a):
    a = a * pi / 180
    buf = x
    x = cos(a) * x - sin(a) * z
    z = cos(a) * z + sin(a) * buf
    return x, y, z


def rotateZ(x, y, z, a):
    a = a * pi / 180
    buf = x
    x = cos(a) * x - sin(a) * y
    y = cos(a) * y + sin(a) * buf
    return x, y, z


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
