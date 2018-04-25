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

        self.bg_color_button.clicked.connect(lambda: get_bg_color(self))
        self.fg_color_button.clicked.connect(lambda: get_fg_color(self))
        
        


def get_bg_color(win):
    color = QtWidgets.QColorDialog.getColor(initial = Qt.white, title = "bg color", options = QtWidgets.QColorDialog.DontUseNativeDialog)

    if color.isValid():
        win.bg_color = color
        win.image.fill(color)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10);
        s.setBackgroundBrush(color);
        win.bg_prev.setScene(s)
        win.scene.setBackgroundBrush(color)

def get_fg_color(win):
    color = QtWidgets.QColorDialog.getColor(initial = Qt.white, title = "fg color", options = QtWidgets.QColorDialog.DontUseNativeDialog)

    if color.isValid():
        win.fg_color = color
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10);
        s.setBackgroundBrush(color);
        win.fg_prev.setScene(s)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
