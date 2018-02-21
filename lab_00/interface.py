#test.py
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
        self.canvas.create_line(350, 0, 350, 600, arrow=tk.FIRST, width=2)
        self.canvas.create_text(375, 10, text='Y(19)')
        self.canvas.create_line(0, 300, 700, 300, arrow=tk.LAST, width=2)
        self.canvas.create_text(675, 310, text='X(22)')
        
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
            self.var.set("| Add(x y splited by spaces)\n| remove(choice string in lsbox to del it)\n| clean(clean all dots)")
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
        tags = self.canvas.gettags(self.canvas.find_closest(x, y, halo=None, start=None))
        self.canvas.delete(tags[1])



    def scale_dot(self, x, y, scale):
        x = 350 + x*scale
        y = 300 - y*scale
        if(x > 700-15 or x < 15 or y < 15 or y > 585):
            return "err", "err"
        return x, y

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
            

    def build_on_click_button(self):
        a1, a2 = self.get_dot_list()
        if(a1 == () and a2 == ()):
            self.debuger_write_info("nothing to build")
            return

        # making ex build
        """
        for a in a1:
            for b in a1:
                for c in a1:
                    if(self.get_triangle(a, b, c)):
                    """
        a = (10, 7)
        b = (6, 6)
        c = (2, 8)
        k = self.get_circle_coords(a, b, c) # getting incenter coords
        print(k)

                        



    def clean_on_click_button(self):
        self.lsbox_1.delete(first=0, last=tk.END)
        self.lsbox_2.delete(first=0, last=tk.END)
        self.canvas.delete("dot")
        self.dotCounter = 0
        self.debuger_write_info("all dots successfully deleted!")



    def show_on_click_button(self):                             # WIP
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
        
        dotObj = self.canvas.find_closest(x, y, halo=None, start=None)
        color = self.canvas.itemcget(dotObj, "fill")
        self.canvas.itemconfigure(dotObj, fill="red")
        self.canvas.itemconfigure(dotObj, fill=color)
        


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
