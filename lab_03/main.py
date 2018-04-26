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
        
        self.circle = True

        self.bg_color_button.clicked.connect(lambda: self.get_bg_color(self))
        self.fg_color_button.clicked.connect(lambda: self.get_fg_color(self))
        self.center_input.returnPressed.connect(lambda: self.get_center_coord(self))
        self.radius_input.returnPressed.connect(lambda: self.get_radius(self))
        self.amount_input.returnPressed.connect(lambda: self.get_amount(self))
        self.step_input.returnPressed.connect(lambda: self.get_step(self))
        
        


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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
