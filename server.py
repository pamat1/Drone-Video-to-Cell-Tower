#!/usr/bin/env python3
from socket import *
import numpy as np

HOST = ''
PORT = 9876
BUFFER_SIZE = 2048

CLIENTS = []

clientsConnected = False

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((HOST, PORT))

print('Server started and listening on port ', PORT,'...\n')


def connect_clients():
    client_one_address = CLIENTS[0]
    client_two_address = CLIENTS[1]
    client_one_reply = 'REROUTINGTO ' + str(client_two_address)
    client_two_reply = 'REROUTINGTO ' + str(client_one_address)
    serverSocket.sendto(client_one_reply.encode(), CLIENTS[0])
    serverSocket.sendto(client_two_reply.encode(), CLIENTS[1])
    clientsConnected = True



while True:
    message, clientAddr = serverSocket.recvfrom(BUFFER_SIZE)
    if not clientAddr in CLIENTS:
        CLIENTS.append(clientAddr)
        reply = "Connection successful"
        serverSocket.sendto(reply.encode(), clientAddr)
        information = "INFO_NEW " + str(clientAddr)
        serverSocket.sendto(information.encode(), clientAddr)
        if (len(CLIENTS) == 2) and (clientsConnected is False):
            connect_clients()

    else:
        message = message.decode()
        print('Message from ', clientAddr, ': ', message, '\n')
        reply = 'Echoing ' + message
        serverSocket.sendto(reply.encode(), clientAddr)
    print('Server still listening on port ', PORT, '...\n')