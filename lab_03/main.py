import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QImage, QPixmap, QRgba64
from PyQt5.QtCore import Qt
from math import sqrt, pi, cos, sin


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("design.ui", self)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 520, 520)
        self.canvas.setScene(self.scene)
        self.image = QImage(520, 520, QImage.Format_ARGB32_Premultiplied)
        self.pen = QPen()
        self.fg_color = QColor(Qt.black)
        self.bg_color = QColor(Qt.white)

        self.center_x = 255
        self.center_y = 255
        self.radius = 100
        self.amount = 30
        self.step = 10
        self.current_alg = "canonical equation"
        
        self.circle.setChecked(True)
        self.ellipse.setChecked(False)

        self.bg_color_button.clicked.connect(lambda: self.get_bg_color(self))
        self.fg_color_button.clicked.connect(lambda: self.get_fg_color(self))
        self.concentric_button.clicked.connect(lambda: self.draw_centr(self))
        self.center_input.returnPressed.connect(lambda: self.get_center_coord(self))
        self.radius_input.returnPressed.connect(lambda: self.get_radius(self))
        self.amount_input.returnPressed.connect(lambda: self.get_amount(self))
        self.step_input.returnPressed.connect(lambda: self.get_step(self))
        self.alg_box.currentIndexChanged.connect(lambda: self.get_algorithm(self))
        
        

    def draw_centr(self, win):
        is_standart = False
        current_alg = self.current_alg
        x = self.center_x
        y = self.center_y
        d = self.step
        c = self.amount


        if win.circle.isChecked():
            for i in range(d, d * c + d, d):

                if current_alg == "canonical equation":
                    self.circle_canon(win, x, y, i)
                if current_alg == "parametric equation":
                    self.circle_param(win, x, y, i)
                if current_alg == "Bresenham":
                    self.circle_brez(win, x, y, i)
                if current_alg == "mid-point":
                    self.circle_middle(win, x, y, i)
                if current_alg == "standart":
                    is_standart = True
                    win.scene.addEllipse(x - i, y - i, i * 2, i * 2, win.pen)

        if not is_standart:
            pix = QPixmap(520, 520)
            pix.convertFromImage(win.image)
            win.scene.addPixmap(pix)
        


    def get_bg_color(self, win):
        color = QtWidgets.QColorDialog.getColor(initial = Qt.white, title = "bg color", options = QtWidgets.QColorDialog.DontUseNativeDialog)

        if color.isValid():
            win.bg_color = color
            win.image.fill(color)
            s = QtWidgets.QGraphicsScene(0, 0, 10, 10);
            s.setBackgroundBrush(color);
            win.bg_prev.setScene(s)
            win.scene.setBackgroundBrush(color)

    def get_fg_color(self, win):
        color = QtWidgets.QColorDialog.getColor(initial = Qt.white, title = "fg color", options = QtWidgets.QColorDialog.DontUseNativeDialog)

        if color.isValid():
            win.fg_color = color
            win.pen.setColor(color)
            s = QtWidgets.QGraphicsScene(0, 0, 10, 10);
            s.setBackgroundBrush(color);
            win.fg_prev.setScene(s)

    def get_center_coord(self, win):
        s = win.center_input.text();
        self.center_x, self.center_y = s.split()
        print(self.center_x, self.center_y)

    def get_radius(self, win):
        s = win.radius_input.text();
        self.radius = float(s)
        print(self.radius)

    def get_amount(self, win):
        s = win.amount_input.text();
        self.amount = int(s)
        print(self.amount)

    def get_step(self, win):
        s = win.step_input.text();
        self.step = int(s)
        print(self.step)

    def get_algorithm(self, win):
        self.current_alg = win.alg_box.currentText()
        print(self.current_alg)


    def circle_canon(self, win, cx, cy, r):
        for x in range(0, r + 1, 1):
            y = round(sqrt(r ** 2 - x ** 2))
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

        for y in range(0, r + 1, 1):
            x = round(sqrt(r ** 2 - y ** 2))

            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())


    def circle_param(self, win, cx, cy, r):
        l = round(pi * r / 2 )
        for i in range(0, l + 1, 1):
            x = round(r * cos(i / r))
            y = round(r * sin(i / r))
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

    def circle_brez(self, win, cx, cy, r):
        x = 0
        y = r
        d = 2 - 2 * r
        while y >= 0:
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

            if d < 0:
                buf = 2 * d + 2 * y - 1
                x += 1

                if buf <= 0:
                    d = d + 2 * x + 1
                else:
                    y -= 1
                    d = d + 2 * x - 2 * y + 2

                continue

            if d > 0:
                buf = 2 * d - 2 * x - 1
                y -= 1

                if buf > 0:
                    d = d - 2 * y + 1
                else:
                    x += 1
                    d = d + 2 * x - 2 * y + 2

                continue

            if d == 0.0:
                x += 1
                y -= 1
                d = d + 2 * x - 2 * y + 2

    def circle_middle(self, win, cx, cy, r):
        x = 0
        y = r
        p = 5 / 4 - r  # (x + 1)^2 + (y - 1/2)^2 - r^2
        while True:
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())

            win.image.setPixel(cx - y, cy + x, win.pen.color().rgb())
            win.image.setPixel(cx + y, cy - x, win.pen.color().rgb())
            win.image.setPixel(cx - y, cy - x, win.pen.color().rgb())
            win.image.setPixel(cx + y, cy + x, win.pen.color().rgb())

            x += 1

            if p < 0:
                p += 2 * x + 1
            else:
                p += 2 * x - 2 * y + 5
                y -= 1

            if x > y:
                break



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
