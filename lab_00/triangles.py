import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.geometry('1000x750')


# create main container
center = tk.Frame(  root, 
                    bg="gray2",
                    width=50,
                    height=40,
                    padx=3,
                    pady=3  )


root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

center.grid(    row=1, 
                sticky="nsew"   )


# create the center widgets
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

ctr_left = tk.Frame(    center,
                        bg="#fff5cb",
                        width=400,
                        height=750   )

ctr_right = tk.Frame(   center,
                        bg="#f7ffcb",
                        width=600,
                        height=750  )

ctr_left.grid(row=0, column=0, sticky="nsew")
ctr_right.grid(row=0, column=1, sticky="nsew")

# create left widgets
#ctr_left.grid_rowconfigure(1, weight=1)
#ctr_left.grid_columnconfigure(0, weight=1)

#create the widgets for the ctr_left frame
lsBox = tk.Listbox(ctr_left)
qButton = tk.Button(ctr_left, text="QUIT", fg="red", command=root.destroy)
entryText = tk.Entry(ctr_left, background = "#ffe9cb")
 
# layout the widgets in the ctr_left frame
lsBox.grid(row=0, columnspan=3)
entryText.grid(row=1, column=0)
qButton.grid(row=4, column=0, sticky="se")


root.mainloop()
