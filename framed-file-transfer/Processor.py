import os, sys, threading
from frameSocket import *

class Processor(threading.Thread):
    #Define files, lock and count of processors
    files = set()
    transferlock = threading.Lock()
    totalprocessors = 0

    #Instantiate a processor
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        Processor.totalprocessors += 1
        self.conn = conn
        self.addr = addr

    #Check if process processed current file or not (file trasnfer), lock while checking.
    def check(self, name):
        self.transferlock.acquire()
        if name in self.files:
            status = False
        else:
            self.files.add(name)
            status = True
        self.transferlock.release()
        return status


    def run(self):
        #Start frame socket
        framesocket = FrameSocket(self.conn)
        framesocket.frameRead()
        
        #Loop through name and byte lists.
        for (name, bytes) in zip(framesocket.namelist, framesocket.bytelist):
            #Check if file has been added
            saveFlag = self.check(name)
            #If so then send data to serverStorage to be saved
            if saveFlag:
                path = os.getcwd() + "/serverStorage/" + name

                if not os.path.exists(path):
                    open(path, 'x')

                    with open(path, 'w') as storageFile:
                        storageFile.write(bytes)
            #Otherwise adjust filename and send data under adjusted filename
            else:
                pos = name.index('.')
                num = int(name[pos - 1])
                newname = "file"+str(num+1)+".txt"
                path = os.getcwd() + "/serverStorage/" + newname

                open(path, 'x')

                with open(path, 'w') as storageFile:
                    storageFile.write(bytes)
        #Send ok signal
        self.conn.send("1".encode())