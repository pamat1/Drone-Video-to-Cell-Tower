from tkinter import *

window = Tk()

log = Text(window)
log.pack()

user = StringVar()
input = Entry(window, text = user)
input.pack(side = BOTTOM, fill = X)

def Enter_pressed(event):
    input_get = input.get()
    print(input_get)
    log.insert(INSERT, '%s\n' % input_get)

    user.set('')
    return "break"

frame = Frame(window)
input.bind("<Return>", Enter_pressed)
frame.pack()

window.mainloop()
