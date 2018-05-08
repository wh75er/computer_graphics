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

        self.current_alg = "canonical equation"
        
        self.circle.setChecked(True)
        self.ellipse.setChecked(False)

        self.bg_color_button.clicked.connect(lambda: self.get_bg_color(self))
        self.fg_color_button.clicked.connect(lambda: self.get_fg_color(self))
        self.concentric_button.clicked.connect(lambda: self.draw_centr(self))
        self.clean_button.clicked.connect(lambda: self.canvas_clean(self))
        self.draw_button.clicked.connect(lambda: self.draw_manual(self))
        self.alg_box.currentIndexChanged.connect(lambda: self.get_algorithm(self))
        
        

    def draw_centr(self, win):
        is_standart = False
        current_alg = self.current_alg
        
        step = int(win.step_input.text())
        amount = int(win.amount_input.text())
        x = 255 
        y = 255
        d = step
        c = amount


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

        if win.ellipse.isChecked():
            for i in range(d, d * c + d, d):
                if current_alg == "canonical equation":
                    self.ellipse_canon(win, x, y, i * 2, i)
                if current_alg == "parametric equation":
                    self.ellipse_param(win, x, y, i * 2, i)
                if current_alg == "Bresenham":
                    self.ellipse_brez(win, x, y, i * 2, i)
                if current_alg == "mid-point":
                    self.ellipse_middle(win, x, y, i * 2, i)
                if current_alg == "standart":
                    is_standart = True
                    win.scene.addEllipse(x - i * 2, y - i, i * 4, i * 2, win.pen)

        if not is_standart:
            pix = QPixmap(520, 520)
            pix.convertFromImage(win.image)
            win.scene.addPixmap(pix)

    def draw_manual(self, win):
        is_standart = False
        current_alg = self.current_alg
        x = win.center_x.value()
        y = win.center_y.value()

        if self.circle.isChecked():
            rad = win.radius.value()
            if current_alg == "canonical equation":
                self.circle_canon(win, x, y, rad)
            if current_alg == "parametric equation":
                self.circle_param(win, x, y, rad)
            if current_alg == "Bresenham":
                self.circle_brez(win, x, y, rad)
            if current_alg == "mid-point":
                self.circle_middle(win, x, y, rad)
            if current_alg == "standart":
                is_standart = True
                win.scene.addEllipse(x - rad, y - rad, rad * 2, rad * 2, win.pen)

        if self.ellipse.isChecked():
            a = win.a_box_input.value()
            b = win.b_box_input.value()
            if current_alg == "canonical equation":
                self.ellipse_canon(win, x, y, b, a)
            if current_alg == "parametric equation":
                self.ellipse_param(win, x, y, b, a)
            if current_alg == "Bresenham":
                self.ellipse_brez(win, x, y, b, a)
            if current_alg == "mid-point":
                self.ellipse_middle(win, x, y, b, a)
            if current_alg == "standart":
                is_standart = True
                win.scene.addEllipse(x - b, y - a, b*2, a*2, win.pen)

        if not is_standart:
            pix = QPixmap(520, 520)
            pix.convertFromImage(win.image)
            win.scene.addPixmap(pix)
        
    def canvas_clean(self, win):
        win.image.fill(self.bg_color)
        win.scene.clear()



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

    def get_algorithm(self, win):
        self.current_alg = win.alg_box.currentText()
        print(self.current_alg)

        
# -------------------------- circle ------------------------------------

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

# -------------------------- ellipse ------------------------------------

    def ellipse_canon(self, win, cx, cy, a, b):
        for x in range(0, a + 1, 1):
            y = round(b * sqrt(1.0 - x ** 2 / a / a))
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

        for y in range(0, b + 1, 1):
            x = round(a * sqrt(1.0 - y ** 2 / b / b))
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

    def ellipse_param(self, win, cx, cy, a, b):
        m = max(a, b)
        l = round(pi * m / 2)
        for i in range(0, l + 1, 1):
            x = round(a * cos(i / m))
            y = round(b * sin(i / m))
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

    def ellipse_brez(self, win, cx, cy, a, b):
        x = 0
        y = b
        a = a ** 2
        d = round(b * b / 2 - a * b * 2 + a / 2)
        b = b ** 2
        while y >= 0:
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
            if d < 0:
                buf = 2 * d + 2 * a * y - a
                x += 1
                if buf <= 0:
                    d = d + 2 * b * x + b
                else:
                    y -= 1
                    d = d + 2 * b * x - 2 * a * y + a + b

                continue

            if d > 0:
                buf = 2 * d - 2 * b * x - b
                y -= 1

                if buf > 0:
                    d = d - 2 * y * a + a
                else:
                    x += 1
                    d = d + 2 * x * b - 2 * y * a + a + b

                continue

            if d == 0.0:
                x += 1
                y -= 1
                d = d + 2 * x * b - 2 * y * a + a + b

    def ellipse_middle(self, win, cx, cy, a, b):
        x = 0  
        y = b
        p = b**2 + (a**2*(1-4*b) - 2)/4
        dp_e = 3*b**2
        d2p_e = 2*b**2
        dp_se = dp_e - 2*a**2*(b - 1)
        d2p_se = d2p_e + 2*a**2

        while dp_se < (2*a**2 + 3*b**2):
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())

            x += 1

            if p < 0:
                p += dp_e
                dp_e += d2p_e
                dp_se += d2p_e
            else:
                y -= 1
                p += dp_se
                dp_e += d2p_e
                dp_se += d2p_se

        p -= (a**2*(4*y - 3) + b**2*(4*x+3) + 2)/4
        dp_s = a**2*(3-2*y)
        dp_se = 2*b**2 + 3*a**2
        d2p_s = 2*a**2

        while y > 0:
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())

            y -= 1

            if p > 0:
                p += dp_s
                dp_s += d2p_s
                dp_se += d2p_s
            else:
                x += 1
                p += dp_se
                dp_s += d2p_s
                dp_se += d2p_se




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
