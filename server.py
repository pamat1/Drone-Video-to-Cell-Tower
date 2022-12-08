#!/usr/bin/env python3
from socket import *

HOST = ''
PORT = 9876
BUFFER_SIZE = 2048

CLIENTS = []

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((HOST, PORT))

print('Server started and listening on port ', PORT,'...\n')

while True:
    message, clientAddr = serverSocket.recvfrom(BUFFER_SIZE)
    if not clientAddr in CLIENTS:
        CLIENTS.append(clientAddr)
        reply = "Connection successful"
        serverSocket.sendto(reply.encode(), clientAddr)
    else:
        message = message.decode()
        print('Message from ', clientAddr, ': ', message, '\n')
        reply = 'Echoing ' + message
        serverSocket.sendto(reply.encode(), clientAddr)
    print('Server still listening on port ', PORT, '...\n')
