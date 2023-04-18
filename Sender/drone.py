import socket
import sys
import threading
import os
import signal
import subprocess
import shlex
import time
from constants import *
from PeripheralFunction import *

rendezvous = ('141.219.64.105', 55555)

# connect to rendezvous
print('connecting to rendezvous server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50001))
sock.sendto(b'0', rendezvous)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

data = sock.recv(1024).decode()
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))
print('  dest port:   {}\n'.format(dport))

# punch hole
# equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
print('punching hole')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
sock.bind(('0.0.0.0', sport))
sock.sendto(b'0', (ip, dport))

print('ready to exchange messages\n')

# listen for
# equiv: nc -u -l 50001
def listen():
    global ip
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(('0.0.0.0', sport))

    pid1 = None
    pid2 = None
    while True:
        data = sock.recv(1024)
        datadec = data.decode()
        print('\rpeer: {}\n> '.format(data.decode()), end='')
        if (datadec == "CMD_START_STREAM_SRT"):
            if (pid2 == None):
                print("./streamfull_hw.sh "+ ip + " " + str(STREAM_PORT))
                proc2 = subprocess.Popen("./streamfull_hw.sh "+ ip + " " + str(STREAM_PORT), shell=True)
                break
            #proc2 = subprocess.call(shlex.split("./send.sh " + ip + " " + str(STREAM_PORT)))
            #out2 = proc2.communicate()[0]
            #pid2 = proc2.pid
        if (datadec == "CMD_STOP_STREAM_SRT"):
            os.kill(pid1, signal.SIGTERM)
            os.kill(pid2, signal.SIGTERM)
            pass

sock.close()
listener = threading.Thread(target=listen, daemon=True)
listener.start()

# send messages
# equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dport))

def sendData():
    BNObus, i2c = initI2C()
    while True:
        msg = "IMU_DATA " + str(read8Data(BNO, BNO055.BNO055_TEMP)) + ' '+str(read16Data(BNO, BNO055.EULER_H_LSB))
        sock.sendto(msg.encode(), (ip, sport))
        time.sleep(3)

data_collector = threading.Thread(target=sendData, daemon=True)
data_collector.start()


while True:
    msg = input('> ')
    sock.sendto(msg.encode(), (ip, sport))
