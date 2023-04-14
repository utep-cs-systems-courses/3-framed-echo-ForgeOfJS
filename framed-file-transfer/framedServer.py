#! /usr/bin/env python3
import socket, sys, re
sys.path.append("../lib")       # for params
import params
from Processor import *

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    )


paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(10)              # allow 10 outstanding requests
print("Listening...")
# s is a factory for connected sockets
# wait until incoming connection request (and accept it)
while 1:
    #accept a connection and give control over to processor class.
    conn, addr = s.accept()
    print('Connected by', addr)

    process = Processor(conn, addr)
    process.start()

os.chdir("serverStorage")
    

