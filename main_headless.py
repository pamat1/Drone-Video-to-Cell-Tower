import socket
import threading
from threading import Thread
from ast import literal_eval
import subprocess
import shlex

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
serverName = "141.219.61.105"  # replace this with whatever the server IP is
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
                if command == 'INFO_NEW':
                    address = literal_eval(text)
                    ADDR = address[0]
                    PORT = address[1]
                if command == 'REROUTINGTO':
                    p2p_addr = literal_eval(text)
                    p2p_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    #p2p_socket.bind((ADDR, PORT))
                    print(p2p_addr)
                    isP2P = True
                if command == 'STREAM_INFO':
                    subprocess.call([r'receive.bat'])  # Replace with equivalent vlc shell script
                    break


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


class AsyncVideoStreaming(Thread):
    def __init__(self, params):
        super().__init__()
        self.response = None
        self.params = params

    def run(self):
        global ADDR
        stream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        stream_socket.bind((ADDR, 6000)) # Replace this wit 9584? I don't understand the 6000 here

        # Tell server 'I'm streaming at this port'
        global server_socket
        command = "STREAM_INFO " + str(9584)  # port we're using for streaming
        server_socket.sendto(command.encode(), p2p_addr)
        subprocess.call(shlex.split('./pipeline.sh ' + str(self.params)))


if __name__ == "__main__":
    server_thread = AsyncServerUpdate()
    server_thread.start()
    p2p_thread = AsyncP2PUpdate()
    p2p_thread.start()
    while not isP2P:
        pass
    if isP2P:
        streaming_thread = AsyncVideoStreaming(9584)
        streaming_thread.start()
