from tkinter import *
from tkinter import Menu
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as font
import os
root=Tk("Text Editor")
APPNAME = "SimpliText"
root.title(f"Untitled - {APPNAME}")
try:
    fnt = font.Font(family="Monoid")
except:
    fnt = font.Font(family="Arial")
text=Text(root) 
text.grid()
text.config(font=fnt)
def on_exit():
    if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
        root.destroy()
def saveas():

    global text
    global APPNAME
    t = text.get("1.0", "end-1c")

    savelocation= filedialog.asksaveasfilename(title="Save As",filetypes = (("All Files","*.*"),))
    x = savelocation.split('/')
    fname = x[len(x)-1]
    root.title(f"{fname} - {APPNAME}")
    try:
        with open(savelocation, "w+") as f:
            f.write(t)
    except:
        messagebox.showerror("Save Error","Could not save file.")

def opn():
    global text
    global root
    global APPNAME
    openlocation = filedialog.askopenfilename(title = "Open",filetypes = (("All Files","*.*"),))
    fname = os.path.basename(openlocation)
    
    try:
        with open(openlocation, "r") as f:
            t = f.read()
            text.delete(1.0,"end")
            text.insert(1.0,t)
            root.title(f"{fname} - {APPNAME}")
    except:
        messagebox.showerror("Open Error","Could not open file.")
    


menubar=Menu(root)
fileMenu = Menu(menubar,tearoff=False)
fileMenu.add_command(label="Open", command=opn)
fileMenu.add_command(label="Save", command=saveas)
menubar.add_cascade(label="File", menu=fileMenu)
optionsMenu = Menu(menubar,tearoff=False)
optionsMenu.add_command(label="Quit", command=on_exit)
menubar.add_cascade(label="Options", menu=optionsMenu)

root.config(menu=menubar)

root.protocol("WM_DELETE_WINDOW", on_exit)


root.mainloop()
