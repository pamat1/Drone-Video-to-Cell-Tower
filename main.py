from tkinter import *
import tkinter as tk
from tkinter import ttk
import sys
import socket
import threading
from threading import Thread
import requests
import time

# Globals

isConnected = False
clientSocket = None
server_socket = None
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
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        hello = "hello"
        server_socket.sendto(hello.encode(), serverAddr)
        isConnected = True
        while True:
            if isConnected:
                self.response = server_socket.recvfrom(2048)
                text = self.response[0].decode()
                print(text)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("GUI Demo")
        self.geometry('600x400')

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

        self.body.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

    def handle_enter_pressed(self, event):
        global isConnected
        global serverAddr
        global server_socket
        input_get = self.user_input.get()


        if isConnected:
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


if __name__ == "__main__":
    app = App()
    app.mainloop()
