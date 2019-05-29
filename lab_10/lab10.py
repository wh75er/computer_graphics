import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QImage, QPixmap, QRgba64, qRgb
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

bg_color = 1
fg_color = 0

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
        self.image = QImage(600, 600, QImage.Format_MonoLSB)

        self.pen = QPen(black)

        self.funcs.addItems(["2 * cos(x * z)",
                            "5*sin(x) - cos(z)",
                            "exp(sin(sqrt(x**2 + z**2)))",
                            "cos(x) * sin(z)",
                            "cos(x**2 + z**2)",
                            "(x**2+z**2)**0.5",
                            "1-abs(x+z)-abs(z-x)"])

        self.pen.setColor(green)
        self.image.setColor(0, qRgb(255, 111, 105))
        self.image.setColor(1, qRgb(0, 0, 0))
        self.image.fill(bg_color)

        self.scene.setBackgroundBrush(QBrush(black))

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
        self.angle_changed(win)


#-----------------   methods   ------------------------------------

    def f(self, x, z):
        return eval(self.funcs.currentText())

    def angle_changed(self, win):
        self.scene.clear()
        self.image.fill(bg_color)
        self.floating_horizon()

        pix = QPixmap()
        pix.convertFromImage(self.image)
        self.scene.addPixmap(pix)


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
                top, bottom, self.image = horizon(xl, yl, xPrev, yPrev, top, bottom, self.image)
            xl = xPrev
            yl = yPrev

            x = xMin
            while x <= xMax:
                y = self.f(x, z)
                xCurr, yCurr, zT = self.transform(x, y, z)

                top, bottom, self.image = horizon(xPrev, yPrev, xCurr, yCurr, top, bottom, self.image)
                xPrev = xCurr
                yPrev = yCurr

                x += xStep

            if z != zMax:
                xr = xMax
                yr = self.f(xr, z-zStep)
                xr, yr, zT = self.transform(xr, yr, z)
                top, bottom, self.image = horizon(xr, yr, xPrev, yPrev, top, bottom, self.image)

            z -= zStep

    def transform(self, x, y, z):
        x, y, z = rotateX(x, y, z, self.x_angle.value())
        x, y, z = rotateY(x, y, z, self.y_angle.value())
        x, y, z = rotateZ(x, y, z, self.z_angle.value())
        x = x * k + shx
        y = y * k + shy
        return round(x), round(y), round(z)



#-----------------   functions  ------------------------------------\

def horizon(x1, y1, x2, y2, top, bottom, image):
    if x2<x1:
        x1, y1, x2, y2 = swap(x1, y1, x2, y2)
    dx = x2-x1
    dy = y2-y1
    if dx>dy:
        steps = dx
    else:
        steps = dy
    if steps:
        xInc = dx/steps
        yInc = dy/steps
    else:
        steps = 1

    x = x1
    y = y1
    for i in range(steps):
        xCurr = round(x)
        yCurr = round(y)
        if yCurr >= top[xCurr]:
            top[xCurr] = y
            image.setPixel(xCurr, yCurr, 0)
        if yCurr <= bottom[xCurr]:
            bottom[xCurr] = y
            image.setPixel(xCurr, yCurr, 0)
        if steps != 1:
            x += xInc
            y += yInc

    return top, bottom, image

def swap(x1, y1, x2, y2):
    return x2, y2, x1, y1

def sign(a):
    if a < 0:
        return -1
    if a == 0:
        return 0
    if a > 0:
        return 1
    return None


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
