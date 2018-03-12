# interface.py
# for all objects you have to use tags, or program will work incorrectly
try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu
import math as m


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


        # calculate figure coordinates
        self.f1_list = []
        self.f2_list = []
        self.f3_list = []
        self.calculate_dots(-1, 1)

        # remember dot list, which we can modify
        self.dot_list = [[], [], []]
        self.create_list_with_dots()
        # initilize image and draw it on canvas
        for i in self.dot_list:
            self.init_img(i)

        # dot list history (for self.dot_list)
        self.dot_list_history = []
        self.remember_dot_stage()





    def rotate_on_button_click(self):
        if(not self.inputStr.get()):
            return
        
        cx, cy, angle = map(float, self.inputStr.get().split())
        angle = m.radians(angle)
        a = self.dot_list
        for i in range(len(a)):
            for j in range(len(a[i])):
                a[i][j][0], a[i][j][1] = cx + (a[i][j][0] - cx)*m.cos(angle) - (a[i][j][1] - cy)*m.sin(angle) \
                                        ,cy + (a[i][j][0] - cx)*m.sin(angle) + (a[i][j][1] - cy)*m.cos(angle)
        self.draw_img(a)
        self.remember_dot_stage()
        self.debuger_write_info("rotate done")


    def move_on_button_click(self):
        if(not self.inputStr.get()):
            return
        
        kx, ky = map(float, self.inputStr.get().split())
        a = self.dot_list
        for i in range(len(a)):
            for j in range(len(a[i])):
                a[i][j][0], a[i][j][1] = a[i][j][0] + kx, a[i][j][1] + ky
        self.draw_img(a)
        self.remember_dot_stage()
        self.debuger_write_info("move done")


    def scale_on_button_click(self):
        if(not self.inputStr.get()):
            return
        
        kx, ky, m1, m2 = map(float, self.inputStr.get().split())
        a = self.dot_list
        for i in range(len(a)):
            for j in range(len(a[i])):
                a[i][j][0], a[i][j][1] = self.scale(a[i][j][0], a[i][j][1], kx, ky, m1, m2)
        self.draw_img(a)
        self.remember_dot_stage()
        self.debuger_write_info("scale done")
                

    def quit_on_button_click(self):
        self.master.quit()


    def back_on_button_click(self):
        if(not len(self.dot_list_history) > 1):
            return

        a = self.dot_list_history
        b = self.dot_list
        for i in range(len(a[len(a)-2][0])):
            b[0][i] = a[len(a)-2][0][i][:]
        for i in range(len(a[len(a)-2][1])):
            b[1][i] = a[len(a)-2][1][i][:]
        for i in range(len(a[len(a)-2][2])):
            b[2][i] = a[len(a)-2][2][i][:]
        del a[len(a)-1]
        
        self.draw_img(b)
        self.debuger_write_info("back step")
        



    def scale(self, x, y, kx, ky, m1, m2):
        return kx * x + (1 - kx)*m1, ky * y + (1 - ky)*m2

    def f1(self, x):
        return x**2
    def f2(self, x):
        return m.exp(x)
    def f3(self, x):
        return m.exp(-x)


    def debuger_write_info(self, s):
        if(self.var.get().count('\n') > 8):
            self.var.set("| Welcome! waiting for commands...\n"
                        "| kx, ky -- move\n"
                        "| kx, ky, xc, yc -- scale\n"
                        "| xc, yc, angle(degr) -- rotate\n")
        self.var.set(self.var.get() + "\n> " + s)

    def draw_img(self, a_arg):
        self.canvas.delete("img")
        for a in a_arg:
            for i in range(len(a)):
                if(i < len(a)-1):
                    self.canvas.create_line(300 + a[i][0], 300 + a[i][1]*(-1), 300 + a[i+1][0], 300 + a[i+1][1]*(-1), tag="img")

    def calculate_dots(self, left_b, right_b):
        i = left_b
        node = [[], []]
        while(i < right_b + 0.06):
            if(i > right_b):
                break
            node[0] = i
            node[1] = self.f1(i)
            self.f1_list.append([node[0], node[1]])
            i += 0.06
        self.f1_list.append([right_b, self.f1(right_b)])
        i = left_b
        node = [[], []]
        while(i < 0.4 + 0.06):
            if(i > 0.4):
                break
            node[0] = i
            node[1] = self.f2(i)
            self.f2_list.append([node[0], node[1]])
            i += 0.06
        self.f2_list.append([0.4, self.f2(0.4)])
        i = -0.4                     #left_b
        node = [[], []]
        while(i < right_b + 0.06):
            if(i > right_b):
                break
            node[0] = i
            node[1] = self.f3(i)
            self.f3_list.append([node[0], node[1]])
            i += 0.06
        self.f3_list.append([right_b, self.f3(right_b)])

    def init_img(self, a):
        for i in range(len(a)):
            if(i < len(a) - 1):
                a[i][0], a[i][1] = self.scale(a[i][0], a[i][1], 250, 250, 0, 0)
                x2, y2 = self.scale(a[i+1][0], a[i+1][1], 250, 250, 0, 0)
                self.canvas.create_line(300 + a[i][0], 300 + a[i][1]*(-1), 300 + x2, 300 + y2*(-1), tag="img") 
        a[i][0], a[i][1] = x2, y2

    def create_list_with_dots(self):
        for i in range(len(self.f1_list)):
            self.dot_list[0].append(self.f1_list[i][:])
        for i in range(len(self.f2_list)):
            self.dot_list[1].append(self.f2_list[i][:])
        for i in range(len(self.f3_list)):
            self.dot_list[2].append(self.f3_list[i][:])

    def remember_dot_stage(self):
        node = [[], [], []]
        for i in range(len(self.dot_list[0])):
            node[0].append(self.dot_list[0][i][:])
        for i in range(len(self.dot_list[1])):
            node[1].append(self.dot_list[1][i][:])
        for i in range(len(self.dot_list[2])):
            node[2].append(self.dot_list[2][i][:])
        self.dot_list_history.append(node)




if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
