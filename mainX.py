from tkinter import *
import tkinter as tk
from tkinter import ttk
import sys
import socket
import threading
from threading import Thread
from ast import literal_eval

# Globals
ADDR = None
PORT = None
isConnected = False
isP2P = False
clientSocket = None
server_socket = None
p2p_socket = None
p2p_addr = None
p2p_port = 9876
serverPort = 9876
serverName = "127.0.0.1"  # localhost
serverAddr = (serverName, serverPort)
responseLock = threading.Lock()


class AsyncServerUpdate(Thread):

    def __init__(self):
        super().__init__()
        self.response = None

    def run(self):
        global isConnected
        global serverAddr
        global server_socket
        global p2p_socket
        global p2p_addr
        global isP2P
        global ADDR
        global PORT
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        hello = "hello"
        server_socket.sendto(hello.encode(), serverAddr)
        isConnected = True
        while True:
            if isConnected:
                self.response = server_socket.recvfrom(2048)
                text = self.response[0].decode()
                print(text)
                command = text.split().pop(0)
                text = text.split(' ', 1)[1]
                print(text)
                
                #Commands:
                
                if command == 'INFO_NEW':
                    address = literal_eval(text)
                    ADDR = address[0]
                    PORT = address[1]
                    
                if command == 'REROUTINGTO':
                    p2p_addr = literal_eval(text)
                    p2p_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    p2p_socket.bind((ADDR, PORT))
                    print(p2p_addr)
                    isP2P = True
                    
                if command == '':    
                

class AsyncP2PUpdate(Thread):
    def __init__(self):
        super().__init__()
        self.response = None
    def run(self):
        global isConnected
        global serverAddr
        global server_socket
        global p2p_socket
        while p2p_socket is None:
            pass
        while True:
            if isP2P:
                self.response = p2p_socket.recvfrom(2048)
                text = self.response[0].decode()
                print(text)




class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("GUI Demo")
        self.geometry('900x500')

        self.create_header_frame()
        self.create_body_frame()

        sys.stdout.write = self.redirect
        sys.stderr.write = self.redirect

    def create_header_frame(self):
        self.header = ttk.Frame(self)

        self.header.columnconfigure(0, weight=1)
        self.header.columnconfigure(1, weight=1)

        # connect button
        self.connect_button = ttk.Button(self.header, text="Connect")
        self.connect_button['command'] = self.handle_connection
        self.connect_button.grid(column=0, row=0, sticky=tk.W)

        self.user = StringVar()
        self.user_input = tk.Entry(self.header, text=self.user)
        self.user_input.grid(column=1, row=0, padx=5, pady=5, sticky=W)
        self.user_input.bind("<Return>", self.handle_enter_pressed)

        self.header.grid(column=0, row=0, padx=10, pady=10, sticky=W)

    def create_body_frame(self):
        self.body = ttk.Frame(self)

        self.log = tk.Text(self.body)
        self.log.pack()
        self.log.grid(column=0, row=1)

        self.input_grid = self.create_input_grid()
        self.input_grid.grid(column = 1, row = 1)

        self.body.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

    def create_input_grid(self):
        self.grid_frame = ttk.Frame(self)
        # Input 1
        # adding a label to the root window
        lbl1 = tk.Label(self.grid_frame, text="Quality:")
        lbl1.grid(column=0, row=0)

        # adding Entry Field
        list1 = tk.Listbox(self.grid_frame, width=10, height=2, selectmode=SINGLE, exportselection=0)
        list1.insert(1, "4k")
        list1.insert(2, "1080p")
        list1.grid(column=1, row=0)

        # Listbox 2
        # adding a label to the root window
        lbl2 = tk.Label(self.grid_frame, text="Encoding:")
        lbl2.grid(column=0, row=1)

        # adding Entry Field
        list2 = tk.Listbox(self.grid_frame, width=10, height=2, selectmode=SINGLE, exportselection=0)
        list2.insert(1, "h.264")
        list2.insert(2, "h.265")
        list2.grid(column=1, row=1)

        # Input 3
        # adding a label to the root window
        lbl3 = tk.Label(self.grid_frame, text="Packet Size:")
        lbl3.grid(column=0, row=2)

        # adding Entry Field
        input3 = tk.Entry(self.grid_frame, width=10)
        input3.grid(column=1, row=2)

        # Input 4
        # adding a label to the root window
        lbl4 = tk.Label(self.grid_frame, text="Minimum Latency:")
        lbl4.grid(column=0, row=3)

        # adding Entry Field
        input4 = tk.Entry(self.grid_frame, width=10)
        input4.grid(column=1, row=3)

        # Input 5
        # adding a label to the root window
        lbl5 = tk.Label(self.grid_frame, text="Round-Trip Time:")
        lbl5.grid(column=0, row=4)

        # adding Entry Field
        input5 = tk.Entry(self.grid_frame, width=10)
        input5.grid(column=1, row=4)

        # Run Test ------------------------------------------------------------

        # adding a label to the root window
        lbl = tk.Label(self.grid_frame, text="Begin SRT")
        lbl.grid(column=0, row=6)



        # function to display text when
        # button is clicked
        def clicked():
            In1 = list1.get()
            In2 = list1.get()
            In3 = input3.get()
            In4 = input4.get()
            print(
                "Test Code" + In1 + In2 + In3 + In4)  # this is where SRT command will be placed with input paramters *****

        # button widget with red color text
        # inside
        btn = tk.Button(self.grid_frame, text="Run Test", fg="red", command=clicked)
        # set Button grid
        btn.grid(column=1, row=6)
        return self.grid_frame

    def handle_enter_pressed(self, event):
        global isConnected
        global serverAddr
        global server_socket
        input_get = self.user_input.get()


        if isP2P:
            p2p_socket.sendto(input_get.encode(), p2p_addr)
            self.log.insert(INSERT, 'Sending to P2P client: ')
        elif isConnected:
            server_socket.sendto(input_get.encode(), serverAddr)
            self.log.insert(INSERT, 'Sending to server: ')


        self.log.insert(INSERT, '%s\n' % input_get)
        self.user_input.delete(0, END)
        return "break"

    def redirect(self, str):
        self.log.insert(INSERT, str)

    def handle_connection(self):

        server_thread = AsyncServerUpdate()
        server_thread.start()
        p2p_thread = AsyncP2PUpdate()
        p2p_thread.start()


if __name__ == "__main__":
    app = App()
    app.mainloop()
