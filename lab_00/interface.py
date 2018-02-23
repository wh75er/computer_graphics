# interface.py
# for all objects you have to use tags, or program will work incorrectly
try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu
import math as m

SCALE = 15


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
        # X-Y axis
        self.canvas.create_line(350, 0, 350, 600, arrow=tk.FIRST, width=2, tag="axis")
        self.canvas.create_text(375, 10, text='Y(19)', tag="axit")
        self.canvas.create_line(0, 300, 700, 300, arrow=tk.LAST, width=2, tag="axit")
        self.canvas.create_text(675, 310, text='X(22)', tag="axit")
        
        self.dotCounter = 0

        # getting ListBox object
        self.lsbox_1 = builder.get_object('lsbox_1', master)
        self.lsbox_1.configure(justify=tk.CENTER)
        self.lsbox_2 = builder.get_object('lsbox_2', master)
        self.lsbox_2.configure(justify=tk.CENTER)




    def get_current_lsbox(self):
        self.lsbox_input = tk.IntVar()
        self.lsbox_input = self.builder.get_variable("_lsbox_now")
        if(self.lsbox_input.get() == 1):
            self.lsbox = self.lsbox_1
        else:
            self.lsbox = self.lsbox_2

    # debuger info 
    def debuger_write_info(self, s):
        self.var = tk.StringVar()
        self.var = self.builder.get_variable("_debug_text")
        if(self.var.get().count('\n') > 8):
            self.var.set("| Add(x y splited by spaces)\n| remove(choice string in lsbox to del it)\n| clean(clean canvas)")
        self.var.set(self.var.get() + "\n> " + s)



    def remove_on_click_button(self):
        self.get_current_lsbox()
        ind = self.lsbox.curselection()
        if(ind == ()):
            self.debuger_write_info("nothing selected")
            return
        ind = ind[0]
        content = self.lsbox.get(first=ind, last=None)
        self.lsbox.delete(first=ind, last=None)
        x = content[0]
        y = content[1]
        self.debuger_write_info("("+str(x)+", "+str(y)+") had been removed")

        # canves working
        x, y = self.scale_dot(x, y, SCALE)
        if(x == "err"):
            self.debuger_write_info("something went wrong")

        tags = self.get_dot_tags(x, y)
        if(not tags):
            raise Exception("Tags suppose to exist")

        a1, a2 = self.get_dot_list()
        if(tuple(content) in a1 or tuple(content) in a2):
            return

        self.canvas.delete(tags[1])



    def get_dot_tags(self, x, y):
        dotObjs = self.canvas.find_overlapping(x, y, x, y)
        tags = []
        for i in dotObjs:
            tags = self.canvas.gettags(i)
            if(tags[0] == "dot"):
                break

        return tags

    def scale_dot(self, x, y, scale):
        x = 350 + x*scale
        y = 300 - y*scale
        if(x > 700-15 or x < 15 or y < 15 or y > 585):
            return "err", "err"
        return x, y

    def get_scale_dot(self, dot, scale):
        dot[0], dot[1] = self.scale_dot(dot[0], dot[1], scale)
        if(dot[0] == "err"):
            raise ValueError("There's error with scaling dot in get_scale_dot function")
        return dot

    def get_dot_list(self):
        a1 = self.lsbox_1.get(first=0, last=tk.END)
        a2 = self.lsbox_2.get(first=0, last=tk.END)
        return a1, a2
    
    def get_triangle(self, a, b, c):
        if( (a[0]-b[0])*(c[1]-b[1]) == (a[1]-b[1])*(c[0]-b[0]) ):
            return 0
        else:
            return 1

    def get_side_len(self, a, b):
        return ( (b[0]-a[0])**2 + (b[1]-a[1])**2 )**(1/2)
    
    def get_circle_coords(self, a, b, c):
        center = list(a)
        la = self.get_side_len(a, b)
        lb = self.get_side_len(b, c)
        lc = self.get_side_len(c, a)
        p = la + lb + lc
        
        if(p):
            center[0] = (lb * a[0] + lc * b[0] + la * c[0])/p
            center[1] = (lb * a[1] + lc * b[1] + la * c[1])/p
        return center

    def build_on_canvas(self, dotLs_1, dotLs_2, crcl_1, crcl_2):
        x1, x2, x3 = dotLs_1[0], dotLs_1[1], dotLs_1[2]
        z1, z2, z3 = dotLs_2[0], dotLs_2[1], dotLs_2[2]

        # scaling values
        x1 = self.get_scale_dot(x1, SCALE)
        x2 = self.get_scale_dot(x2, SCALE)
        x3 = self.get_scale_dot(x3, SCALE)
        z1 = self.get_scale_dot(z1, SCALE)
        z2 = self.get_scale_dot(z2, SCALE)
        z3 = self.get_scale_dot(z3, SCALE)
        crcl_1 = self.get_scale_dot(crcl_1, SCALE)
        crcl_2 = self.get_scale_dot(crcl_2, SCALE)
        
        # build triangles
        self.canvas.create_line(x1[0], x1[1], x2[0], x2[1], width=2, fill="red", tag="ex")
        self.canvas.create_line(x2[0], x2[1], x3[0], x3[1], width=2, fill="red", tag="ex")
        self.canvas.create_line(x3[0], x3[1], x1[0], x1[1], width=2, fill="red", tag="ex")

        self.canvas.create_line(z1[0], z1[1], z2[0], z2[1], width=2, fill="red", tag="ex")
        self.canvas.create_line(z2[0], z2[1], z3[0], z3[1], width=2, fill="red", tag="ex")
        self.canvas.create_line(z3[0], z3[1], z1[0], z1[1], width=2, fill="red", tag="ex")

        # build line between triangles
        self.canvas.create_line(crcl_1[0], crcl_1[1], crcl_2[0], crcl_2[1], width=1, fill="red", tag="ex")


    def build_on_click_button(self):                        #WIP
        self.canvas.delete("ex")
        min_angle = 90
        triangle_1 = [[], [], []]
        triangle_2 = [[], [], []]
        crcl = [[], []]
        a1, a2 = self.get_dot_list()
        if(a1 == () and a2 == ()):
            self.debuger_write_info("nothing to build")
            return

        # making ex build
        for i in range(len(a1)):
            for j in range(i, len(a1)):
                for k in range(j, len(a1)):
                    if(self.get_triangle(a1[i], a1[j], a1[k])):

                        for q in range(len(a2)):
                            for w in range(q, len(a2)):
                                for e in range(w, len(a2)):
                                    if(self.get_triangle(a2[q], a2[w], a2[e])):
                                        circle_1 = self.get_circle_coords(a1[i], a1[j], a1[k])
                                        circle_2 = self.get_circle_coords(a2[q], a2[w], a2[e])
                                        if(circle_1[0] == circle_2[0]):
                                            min_angle = 0
                                            triangle_1[0], triangle_1[1], triangle_1[2] = list(a1[i]), list(a1[j]), list(a1[k])
                                            triangle_2[0], triangle_2[1], triangle_2[2] = list(a2[q]), list(a2[w]), list(a2[e])
                                            crcl[0], crcl[1] = circle_1, circle_2
                                            self.build_on_canvas(triangle_1, triangle_2, circle_1, circle_2)
                                            return
                                        elif(circle_1[1] == circle_2[1] and min_angle == 90):
                                            triangle_1[0], triangle_1[1], triangle_1[2] = list(a1[i]), list(a1[j]), list(a1[k])
                                            triangle_2[0], triangle_2[1], triangle_2[2] = list(a2[q]), list(a2[w]), list(a2[e])
                                            crcl[0], crcl[1] = circle_1, circle_2
                                        else:
                                            a = abs(circle_1[0] - circle_2[0])  # x side of triangle
                                            b = abs(circle_1[1] - circle_2[1])  # y side of triangle
                                            angle = m.degrees(m.atan(b/a))                 # angle between a and c sides of triangle
                                            if(angle < min_angle):
                                                min_angle = angle
                                                triangle_1[0], triangle_1[1], triangle_1[2] = list(a1[i]), list(a1[j]), list(a1[k])
                                                triangle_2[0], triangle_2[1], triangle_2[2] = list(a2[q]), list(a2[w]), list(a2[e])
                                                crcl[0], crcl[1] = circle_1, circle_2
        if(triangle_1 != [[], [], []]):
            self.build_on_canvas(triangle_1, triangle_2, crcl[0], crcl[1])


    def clean_on_click_button(self):
        self.lsbox_1.delete(first=0, last=tk.END)
        self.lsbox_2.delete(first=0, last=tk.END)
        self.canvas.delete("ex")
        self.canvas.delete("dot")
        self.dotCounter = 0
        self.debuger_write_info("canvas  successfully cleared!")



    def show_on_click_button(self):
        self.get_current_lsbox()
        ind = self.lsbox.curselection()
        if(ind == ()):
            self.debuger_write_info("nothing selected")
            return
        ind = ind[0]
        content = self.lsbox.get(first=ind, last=None)
        x = content[0]
        y = content[1]

        x, y = self.scale_dot(x, y, SCALE)
        if(x == "err"):
            self.debuger_write_info("something went wrong")
            return
        
        # get object
        tags = self.get_dot_tags(x, y)
        if(not tags):
            raise Exception("Tags suppose to exist")

        # have to get text object, to get number of dot
        objs = self.canvas.find_withtag(tags[1])
        text = self.canvas.itemcget(objs[0], "text")
        self.debuger_write_info( "dot("+str(content[0])+", "+str(content[1])+") # "+text )
        


    def add_on_click_button(self):
        # taking string from input
        self.inputStr = tk.StringVar()
        self.inputStr = self.builder.get_variable("_input_text")
        # watching to witch lsbox we will add obj
        self.get_current_lsbox()

        if(not self.inputStr.get()):
            return

        node = []
        x, y = map(float, self.inputStr.get().split())
        node.append(x)
        node.append(y)

        x, y = self.scale_dot(x, y, SCALE)
        if(x == "err"):
            self.debuger_write_info("("+str(node[0])+", "+str(node[1])+") is unreachable")
            return

        # dont add existed dots
        a1, a2 = self.get_dot_list()
        if(self.lsbox == self.lsbox_1 and tuple(node) in a1
        or self.lsbox == self.lsbox_2 and tuple(node) in a2):
            self.debuger_write_info("("+str(node[0])+", "+str(node[1])+") already exists")
            return

        self.lsbox.insert(tk.END, node)

        # print that string to output
        self.debuger_write_info("("+str(node[0])+", "+str(node[1])+") had been added")
        self.inputStr.set("")

        if(tuple(node) in a1 or tuple(node) in a2):
            return

        self.dotCounter += 1
        self.canvas.create_text(x+10, y-10, fill="red", text=str(self.dotCounter), tag=("dot", "dot"+str(self.dotCounter)))
        self.canvas.create_oval(x-3, abs(y-3), x+3, abs(y+3), fill="black", width=0, tag=("dot","dot"+str(self.dotCounter)))



    def quit_on_button_click(self):
        self.master.quit()




if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
