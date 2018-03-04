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
        self.centerObj = self.canvas.create_oval(300-2, 300-2, 300+2, 300+2, width=2, fill="black", tag="center")
        # tkinter variables
            # debugger variable
        self.var = tk.StringVar()
        self.var = self.builder.get_variable("_debug_text")
            # input variable
        self.inputStr = tk.StringVar()
        self.inputStr = self.builder.get_variable("_input_text")


        # draw main figure
        self.dotLs = []                                         # original dots
        self.calculate_dots(-0.7, 0.7)
        self.modDots = []                                       # modificated dots
        for i in range(len(self.dotLs)):
            self.modDots.append(self.dotLs[i][:])
        self.init_img()

        # memory steps
        self.memoryL = []




    def scale(self, x, y, kx, ky, m1, m2):
        return kx * x + (1 - kx)*m1, ky * y + (1 - ky)*m2

    def f1(self, x):
        return x**2
    def f2(self, x):
        return m.exp(x)
    def f3(self, x):
        return m.exp(-x)



    def scale_on_button_click(self):
        if(not self.inputStr.get()):
            return
        
        a = self.modDots
        kx, ky, m1, m2 = map(float, self.inputStr.get().split())
        for i in range(len(a)):
            a[i][0], a[i][1] = self.scale(a[i][0], a[i][1], kx, ky, m1, m2)
        self.draw_img()
                

    def quit_on_button_click(self):
        self.master.quit()


    def debuger_write_info(self, s):
        if(self.var.get().count('\n') > 8):
            self.var.set("| Welcome! waiting for commands...\n")
        self.var.set(self.var.get() + "\n> " + s)

    def draw_img(self):
        self.canvas.delete("img")
        for i in range(len(self.modDots)):
            if(i < len(self.modDots)-1):
                self.canvas.create_line(300 + self.modDots[i][0], 300 + self.modDots[i][1]*(-1), 300 + self.modDots[i+1][0], 300 + self.modDots[i+1][1]*(-1), tag="img")

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

    def init_img(self):
        for i in range(len(self.modDots)):
            if(i < len(self.modDots) - 1):
                self.modDots[i][0], self.modDots[i][1] = self.scale(self.modDots[i][0], self.modDots[i][1], 300, 300, 0, 0)
                x2, y2 = self.scale(self.modDots[i+1][0], self.modDots[i+1][1], 300, 300, 0, 0)
                self.canvas.create_line(300 + self.modDots[i][0], 300 + self.modDots[i][1]*(-1), 300 + x2, 300 + y2*(-1), tag="img") 
        self.modDots[i][0], self.modDots[i][1] = x2, y2




if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
