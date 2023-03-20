import socket
from ast import literal_eval
import subprocess
import time
import shlex

# Globals
isConnected = False
middlemanName = "141.219.64.105"
middlemanPort = 9876
middlemanAddr = (middlemanName, middlemanPort)
mmSocket = None
thisAddr = None

isP2P = False
p2pAddr = None
p2pName = None
p2pPort = None
p2pSocket = None

streamName = None
streamPort = None
streamAddr = None

if __name__ == '__main__':
    # Attempt to connect to middleman server
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
    # Once connected, wait for a 'REROUTINGTO' command
    while True:
        if isConnected:
            mmResponse = mmSocket.recvfrom(2048)
            text = mmResponse[0].decode()
            print("Response[0]: " + text)
            command = text.split().pop(0)
            text = text.split(' ', 1)[1]
            print("Command: " + command)
            print("Trimmed response: " + text)
            if command == 'INFO_NEW':
                thisAddr = literal_eval(text)
            if command == 'REROUTINGTO':
                p2pAddr = literal_eval(text)
                p2pName = p2pAddr[0]
                p2pPort = p2pAddr[1]
                p2pSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                print("Rerouting to: " + str(p2pAddr))
                isP2P = True
        if isP2P:
            stream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            stream_socket.bind(thisAddr)
            response = stream_socket.recvfrom(2048)
            print(response)
            command = "STREAM_INFO " + str(9584)
            stream_socket.sendto(command.encode(), p2pAddr)
            subprocess.call(shlex.split('./pipeline.sh ' + str(9584)))
            break
    while True:  # idle until done
        pass
