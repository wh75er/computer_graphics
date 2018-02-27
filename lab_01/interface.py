# interface.py
# for all objects you have to use tags, or program will work incorrectly
try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu
import math as m
import numpy as np


class Application:
    def __init__(self, master):

        self.master = master

        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file('interface.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('main_frame', master)

        builder.connect_callbacks(self)
        

        self.canvas = builder.get_object('canvas', master)

        # draw center of canvas
        self.canvas.create_oval(300-2, 300-2, 300+2, 300+2, width=2, fill="black")

        # draw main figure
        self.dotLs = []
        self.calculate_dots(-0.7, 0.7)
        self.draw_im()


    def scale(self, x, y, kx, ky, m1, m2):
        return kx * x + (1 - kx)*m1, ky * y + (1 - ky)*m2

    def draw_im(self):
        for i in range(len(self.dotLs)):
            if(i < len(self.dotLs) - 1):
                x1, y1 = self.scale(self.dotLs[i][0], self.dotLs[i][1], 80, 80, 0, 0)
                x2, y2 = self.scale(self.dotLs[i+1][0], self.dotLs[i+1][1], 80, 80, 0, 0)
                self.canvas.create_line(300 + x1, 300 + y1*(-1), 300 + x2, 300 + y2*(-1))

    def f1(self, x):
        return x**2
    def f2(self, x):
        return m.exp(x)
    def f3(self, x):
        return m.exp(-x)

    def calculate_dots(self, left_b, right_b):
        i = left_b
        node = [[], []]
        while(i < right_b + 0.1):
            i = round(i, 1)
            if(i > right_b):
                break
            node[0] = i
            node[1] = round(self.f1(i), 1)
            self.dotLs.append([node[0], node[1]])
            i += 0.1
        i = right_b
        while(i > -0.1):
            i = round(i, 1)
            if(i < 0.0):
                break
            node[0] = i
            node[1] = round(self.f3(i), 1)
            self.dotLs.append([node[0], node[1]])
            i -= 0.1
        i = 0
        while(i > left_b - 0.1):
            i = round(i, 1)
            if(i < left_b):
                break
            node[0] = i
            node[1] = round(self.f2(i), 1)
            self.dotLs.append([node[0], node[1]])
            i -= 0.1



    def quit_on_button_click(self):
        self.master.quit()




if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
