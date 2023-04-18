
# Import Module
from tkinter import *
 
# create root window
root = Tk()
 
# root window title and dimension
root.title("SRT Testing GUI")
# Set geometry(widthxheight)
root.geometry('350x200')

# Input Parameters ------------------------------------------------------------

# Input 1
# adding a label to the root window
lbl1 = Label(root, text = "Quality:")
lbl1.grid(column =0, row =0)

# adding Entry Field
list1 = Listbox(root, width=10, height=2, selectmode=SINGLE, exportselection=0)
list1.insert(1, "4k")
list1.insert(2, "1080p")
list1.grid(column =1, row =0)

# Listbox 2
# adding a label to the root window 
lbl2 = Label(root, text = "Encoding:")
lbl2.grid(column =0, row =1)

# adding Entry Field
list2 = Listbox(root, width=10, height=2, selectmode=SINGLE, exportselection=0)
list2.insert(1, "h.264")
list2.insert(2, "h.265")
list2.grid(column =1, row =1)

# Input 3
# adding a label to the root window 
lbl3 = Label(root, text = "Packet Size:")
lbl3.grid(column =0, row =2)

# adding Entry Field
input3 = Entry(root, width=10)
input3.grid(column =1, row =2)

# Input 4
# adding a label to the root window 
lbl4 = Label(root, text = "Minimum Latency:")
lbl4.grid(column =0, row =3)

# adding Entry Field
input4 = Entry(root, width=10)
input4.grid(column =1, row =3)

# Input 5
# adding a label to the root window 
lbl5 = Label(root, text = "Round-Trip Time:")
lbl5.grid(column =0, row =4)

# adding Entry Field
input5 = Entry(root, width=10)
input5.grid(column =1, row =4)

# Run Test ------------------------------------------------------------

# adding a label to the root window
lbl = Label(root, text = "Begin SRT")
lbl.grid(column =0, row =6)
 
# function to display text when
# button is clicked
def clicked():
    In1 = list1.get()
    In2 = list1.get()
    In3 = input3.get()
    In4 = input4.get()
    print("Test Code"+ In1 + In2 + In3 + In4) # this is where SRT command will be placed with input paramters *****
 
# button widget with red color text
# inside
btn = Button(root, text = "Run Test" , fg = "red", command=clicked)
# set Button grid
btn.grid(column=1, row=6)
 
# Execute Tkinter
root.mainloop()
