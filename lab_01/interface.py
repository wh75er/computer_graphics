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
        canterObj = self.canvas.create_oval(300-2, 300-2, 300+2, 300+2, width=2, fill="black", tag="center")

        # draw main figure
        self.dotLs = []                                         # original dots
        self.calculate_dots(-0.7, 0.7)
        self.modDots = []                                       # modificated dots
        for i in range(len(self.dotLs)):
            self.modDots.append(self.dotLs[i][:])
        self.draw_im()




    def scale(self, x, y, kx, ky, m1, m2):
        return kx * x + (1 - kx)*m1, ky * y + (1 - ky)*m2

    def f1(self, x):
        return x**2
    def f2(self, x):
        return m.exp(x)
    def f3(self, x):
        return m.exp(-x)




    def quit_on_button_click(self):
        self.master.quit()



    def draw_im(self):
        print(self.modDots)
        print(self.dotLs)
        for i in range(len(self.dotLs)):
            if(i < len(self.dotLs) - 1):
                self.modDots[i][0], self.modDots[i][1] = self.scale(self.modDots[i][0], self.modDots[i][1], 300, 300, 0, 0)
                x2, y2 = self.scale(self.modDots[i+1][0], self.modDots[i+1][1], 300, 300, 0, 0)
                self.canvas.create_line(300 + self.modDots[i][0], 300 + self.modDots[i][1]*(-1), 300 + x2, 300 + y2*(-1))


    def calculate_dots(self, left_b, right_b):
        i = left_b
        node = [[], []]
        while(i < right_b + 0.06):
            if(i > right_b):
                break
            node[0] = i
            node[1] = self.f1(i)
            self.dotLs.append([node[0], node[1]])
            i += 0.06
        i = right_b
        while(i > -0.06):
            if(i < 0.0):
                break
            node[0] = i
            node[1] = self.f3(i)
            self.dotLs.append([node[0], node[1]])
            i -= 0.06
        i = 0
        while(i > left_b - 0.06):
            if(i < left_b):
                break
            node[0] = i
            node[1] = self.f2(i)
            self.dotLs.append([node[0], node[1]])
            i -= 0.06
        self.dotLs.append([-0.7, 0.49])





if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
