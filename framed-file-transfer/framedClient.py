#! /usr/bin/env python3
import socket, sys, re
from frameSocket import *
sys.path.append("../lib")       # for params

#Archiver updated from lab 1
#NOTE len of file name and bytes are limited by digits, which limits the name size and byte size of transferable files. (Ofc, only really byte size)
def archiver(filelist):
    archivedbytes = bytearray()
    for filename in filelist:
        path = "fileStorage/" + filename
        with open(path, 'rb') as file:
            tempbytes = bytearray(file.read())
        tempfile = f"{'%03d' % len(filename)}".encode() + filename.encode()
        archivedbytes = archivedbytes + tempfile + f"{'%08d' % len(tempbytes)}".encode() + tempbytes
        print(archivedbytes)
    return archivedbytes

# switchesVarDefaults = (
#     (('-s', '--server'), 'server', "127.0.0.1:50001"))

# paramMap = params.parseParams(switchesVarDefaults)

# server  = paramMap["server"]

#Parammap was giving issues, hardcoded server credentials
serverHost = "127.0.0.1"
serverPort = 50001

#Try to create a socket, once socket is created try to establish a connection to the server, if either doens't work, loop through and try again. 
s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

#If socket could not be opened, notify user and exit.
if s is None:
    print('could not open socket')
    sys.exit(1)


while 1:
    #Obtain files requested from user and archive them into a single byte array.
    filelist = input()
    files = filelist.split()

    archivedfiles = archiver(files)
    framewriter = FrameSocket(s)
    #Send archived byte array to frameWriter.
    framewriter.frameWrite(archivedfiles)

    status = int(s.recv(1024).decode())
    #Check if the transfer worked and notify user of either outcome.
    if (status):
        print("Worked.")
        s.close()
        sys.exit(1)
    elif (not status):
        print("Didn't work.")
        s.close()
        sys.exit(0)

