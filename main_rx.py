import socket
from ast import literal_eval
import subprocess
import time

# Globals
isConnected = False
middlemanName = "141.219.64.105"
middlemanPort = 9876
middlemanAddr = (middlemanName, middlemanPort)
mmSocket = None

HOST = ''
thisName = None
thisPort = None
thisAddr = None

isP2P = False
p2pAddr = None
p2pName = None
p2pPort = None
p2pSocket = None

streamName = None
streamPort = None
streamAddr = None
isStreaming = False

if __name__ == '__main__':
    #Attempt to connect to middleman server
    while (isConnected is False):
        print("Attempting to connect to server " + str(middlemanAddr) + "...")
        time.sleep(2)
        try:
            mmSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            hello = "hello"
            mmSocket.sendto(hello.encode(), middlemanAddr)
            isConnected = True
        except:
            continue
    print("Connected to server at " + str(middlemanAddr))
    #Once connected, wait for a 'REROUTINGTO' command
    while True:
        if isP2P:
            print("Waiting for P2P response...")
            p2pResponse = p2pSocket.recvfrom(2048)
            print("received")
            text = p2pResponse[0].decode()
            print("P2PResponse[0]: " + text)
            command = text.split(' ', 1)[1]
            print("Command: " + command)
            print("Trimmed response: " + text)
            if command == 'STREAM_INFO':
                print("Beginning Streaming... ")
                streamPort = literal_eval(text)
                streamAddr = p2pAddr[0] + ":" + str(streamPort)
                isStreaming = True
        if isStreaming:
            break
        if isConnected:
            mmResponse = mmSocket.recvfrom(2048)
            text = mmResponse[0].decode()
            print("Response[0]: " + text)
            command = text.split().pop(0)
            text = text.split(' ', 1)[1]
            print("Command: " + command)
            print("Trimmed response: " + text)
            if command == 'INFO_NEW':
                thisName = literal_eval(text)[0]
                thisPort = literal_eval(text)[1]
                thisAddr = (thisName, thisPort)
            if command == 'REROUTINGTO':
                p2pAddr = literal_eval(text)
                p2pName = p2pAddr[0]
                p2pPort = p2pAddr[1]

                p2pSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                p2pSocket.bind(thisAddr)
                print("Rerouting to: " + str(p2pAddr))
                print("Created new socket for " + str(thisAddr))
                isP2P = True

    subprocess.call([r'receive.bat', streamAddr])
