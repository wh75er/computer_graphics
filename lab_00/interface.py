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


    # debuger info 
    def debuger_write_info(self, s):
        self.var = tk.StringVar()
        self.var = self.builder.get_variable("_debug_text")
        if(self.var.get().count('\n') > 8):
            self.var.set("> Add(x y splited by spaces)\n> remove(choice point in lsbox)\n> clean(clean all dots)")
        self.var.set(self.var.get() + "\n> " + s)

    def add_on_click_button(self):
        # taking string from input
        self.inputStr = tk.StringVar()
        self.inputStr = self.builder.get_variable("_input_text")
        # print that string to output
        self.debuger_write_info(self.inputStr.get())
        self.inputStr.set("")

    def quit_on_button_click(self):
        self.master.quit()


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
