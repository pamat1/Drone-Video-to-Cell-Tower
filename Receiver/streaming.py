import socket
import os
import signal
import subprocess
import shlex
from threading import Thread
from constants import *
from tkinter import *


def holepunch(serverOutput):
    serverOutput.insert(INSERT, "\nStarting holepunch for chat")
    rendezvous = (SERVER_IP, SERVER_PORT)
    # connect to rendezvous
    serverOutput.insert(INSERT, "\nConnecting to rendezvous server")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', CHAT_PORT))
    sock.sendto(b'0', rendezvous)

    while True:
        data = sock.recv(1024).decode()
        if data.strip() == 'ready':
            serverOutput.insert(INSERT, "\nChecked in with server, waiting")
            break

    data = sock.recv(1024).decode()
    ip, sport, dport = data.split(' ')
    sport = int(sport)
    dport = int(dport)

    serverOutput.insert(INSERT, '\nGot peer')
    print('  ip:          {}'.format(ip))
    print('  source port: {}'.format(sport))
    print('  dest port:   {}\n'.format(dport))

    # punch hole
    # equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
    serverOutput.insert(INSERT, '\nPunching hole')
    return ip, sport, dport, sock


class P2P_Chat_Thread(Thread):
    def __init__(self, ip, sport, dport, sock,peerOutput=None, dataOutput=None):
        super().__init__()
        self.ip = ip
        self.sport = sport
        self.dport = dport
        self.sock = sock
        self.peerOutput = peerOutput
        self.dataOutput = dataOutput
        self.dsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dsock.bind(('0.0.0.0', self.dport))

    def sendMsg(self, text):
        msg = text
        self.peerOutput.insert(INSERT, '\n> ' + msg)
        self.dsock.sendto(msg.encode(), (self.ip, self.sport))

    def display(self, text):
        self.peerOutput.insert(INSERT, text)

    def startStream(self):
        msg = "CMD_START_STREAM_SRT"
        self.sock.sendto(msg.encode(), (self.ip, self.sport))

    def stopStream(self):
        msg = "CMD_STOP_STREAM_SRT"
        self.sock.sendto(msg.encode(), (self.ip, self.sport))

    def run(self):
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        #self.sock.bind(('0.0.0.0', self.sport))
        def listen():
            while True:
                data = self.sock.recv(1024)
                data_split = data.decode().split()
                print(data)
                if (data_split[0] == "IMU_DATA"):
                    self.dataOutput.delete(0)
                    self.dataOutput.insert(0, "Temp (C): " + data_split[1])
                    self.dataOutput.delete(1)
                    self.dataOutput.insert(1, "Heading: " + data_split[2])
                else:
                    self.display('\n\rpeer: {}'.format(data.decode()))

        # sock.close()
        listener = Thread(target=listen, daemon=True);
        listener.start()

        # send messages
        # equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
        
        self.display('ready to chat and receive stream\n')

class P2P_Stream_Thread(Thread):
    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self.pid = None
    def startStream(self):
        subprocess.Popen('./rx.sh ' + self.ip + ' ' + str(STREAM_PORT), shell=True)
    def stopStream(self):
        os.kill(self.pid, signal.SIGTERM)
        self.pid = None
        pass
    def run(self):
        pass

