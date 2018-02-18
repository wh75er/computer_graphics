#test.py
try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu


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
        self.canvas.create_text(360, 10, text='Y')
        self.canvas.create_line(0, 300, 700, 300, arrow=tk.LAST, width=2)
        self.canvas.create_text(690, 310, text='X')

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
        choice = self.lsbox.curselection()
        if(choice != ()):
            print(choice[0])
        self.debuger_write_info(str(choice))



    def clean_on_click_button(self):
        self.lsbox_1.delete(first=0, last=tk.END)
        self.lsbox_2.delete(first=0, last=tk.END)
        self.debuger_write_info("All dots successfully deleted!")



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
        self.lsbox.insert(tk.END, node)

        # print that string to output
        self.debuger_write_info("Dot("+str(x)+", "+str(y)+") had been added")

        self.inputStr.set("")



    def quit_on_button_click(self):
        self.master.quit()




if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
