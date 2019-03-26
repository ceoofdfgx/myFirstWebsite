# -*- coding: UTF-8 -*-

import socket
sock = socket.socket()
host = socket.gethostname()
port = 8080
sock.connect((host,port))
print sock.recv(1024)
sock.close()