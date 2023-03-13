import sys
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


isP2P = False
p2pAddr = None
p2pName = None
p2pPort = None
p2pSocket = None

streamName = None
streamPort = None
streamAddr = None

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
        if isConnected:
            mmResponse = mmSockte.recvfrom(2048)
            text = mmResponse[0].decode()
            print("Response[0]: " + text)
            command = text.split().pop(0)
            text = text.split(' ', 1)[1]
            print("Command: " + command)
            print("Trimmed response: " + text)
            if command == 'REROUTINGTO':
                p2pAddr = literal_eval(text)
                p2pName = p2pAddr[0]
                p2pPort = p2pAddr[1]
                p2pSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                print("Rerouting to: " + str(p2pAddr))
                isP2P = True
                continue
            if command == 'STREAM_INFO':
                streamPort = literal_eval(text)
                streamAddr = p2pAddr[0] + ":" + str(streamPort)
                break
    subprocess.call([r'receive.bat', streamAddr])
