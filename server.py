#!/usr/bin/env python3
from socket import *

HOST = ''
PORT = 9876
BUFFER_SIZE = 2048

CLIENTS = []

clientsConnected = False

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((HOST, PORT))

print('Server started and listening on port ', PORT,'...\n')


def connect_clients():
    client_one_address = CLIENTS[1]
    client_two_address = CLIENTS[2]
    client_one_reply = 'REROUTINGTO ' + client_two_address
    client_two_reply = 'REROUTINGTO ' + client_one_address
    serverSocket.sendto(client_one_reply.encode, CLIENTS[1])
    serverSocket.sendto(client_two_reply.encode, CLIENTS[2])
    clientsConnected = True



while True:
    message, clientAddr = serverSocket.recvfrom(BUFFER_SIZE)
    if not clientAddr in CLIENTS:
        CLIENTS.append(clientAddr)
        if (len(CLIENTS) == 2) and (clientsConnected is False):
            connect_clients()
        reply = "Connection successful"
        serverSocket.sendto(reply.encode(), clientAddr)
    else:
        message = message.decode()
        print('Message from ', clientAddr, ': ', message, '\n')
        reply = 'Echoing ' + message
        serverSocket.sendto(reply.encode(), clientAddr)
    print('Server still listening on port ', PORT, '...\n')