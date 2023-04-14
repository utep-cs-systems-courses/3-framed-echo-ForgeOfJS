import socket, re, sys, time

class FrameSocket:
    #Define a size and list for names and bytes as well as the actual byte and name characters
    bytesize = 0
    namesize = 0
    currentbytes = ""
    currentname = ""
    namelist = []
    bytelist = []
    #Flag needed for determining if data is being extracted or if name is being extracted. 
    extractFlag = False

    #Create a socket
    def __init__(self, socket):
        self.socket = socket

    #
    def frameWrite(self, files):
        sent = self.socket.send(files)
        files = files[sent:]

    #Read through data and process names/bytes in an ordered manner
    def frameRead(self):
        while 1:
            #Recieve data and check if the data is empty
            data = self.socket.recv(1024).decode()
            if len(data) == 0:
                #If so, empty lists and reset the current data
                self.updateLists()
                self.resetData()
                break

            while len(data):
                #While there are bytes to process
                print(data, "\n", self.namelist, self.bytelist)
                #Check if name is first in byte array
                if self.namesize == 0 and not self.extractFlag:
                    #If so add namesize and move data forward by namesize
                    try:
                        self.namesize = int(data[:3])
                        data = data[3:]
                    except:
                        print("Size of name not valid")
                #Check if data is first in byte array
                if self.bytesize == 0 and self.extractFlag:
                    #If so add bytesize and move data forward by bytesize
                    try:
                        self.bytesize = int(data[:8])
                        data = data[8:]
                    except:
                        print("Size of data not valid")
                    time.sleep(1)
                
                datalength = len(data)

                #If name was absorbed
                if self.namesize > 0:
                    data = self.getName(datalength= datalength, data= data)
                #If file data was absorbed
                elif self.bytesize > 0:
                    data = self.getBytes(datalength= datalength, data= data)
            #If there was no file or name data to absorb and set to not extract data, finish.
            if self.namesize == 0 and self.bytesize == 0 and not self.extractFlag: break
    
    #Obtain name and check if name is invalid length
    def getName(self, data, datalength):
        #If the there is data beyond the name
        if datalength >= self.namesize:
            #Adjust name by namesize, currentname, namesize, namelist, and set extractFlag to true as data is expected next
            filename = data[0:self.namesize]
            data = data[self.namesize:]
            self.currentname += filename
            self.namesize = 0
            self.namelist.append(self.currentname)
            self.currentname = ""
            self.extractFlag = True
        #If there is less name than namesize describes
        elif datalength < self.namesize:
            #Edge case if data is only 1 character
            if datalength == 1:
                filename = data[0]
            else:
                filename = data[0:datalength]
            #Alter data and adjust name and namesize as name was not fully accepted. 
            data = data[datalength:]
            self.namesize -= datalength
            self.currentname = self.currentname + filename
        return data
    
    #Obtain bytes and check if bytes is invalid length
    def getBytes(self, datalength, data):
        if datalength >= self.bytesize:
            filebytes = data[0:self.bytesize]
            data = data[self.bytesize:]
            #Adjust data by bytesize, currentbytes, namesize, namelist, and set extractFlag to false as name is expected next
            self.currentbytes += filebytes
            self.bytesize = 0
            self.bytelist.append(self.currentbytes)
            self.currentbytes = ""
            self.extractFlag = False
        #If tere is less data than bytesize describes
        elif datalength < self.bytesize:
            #Edge case if name is only one character
            if datalength == 1:
                filebytes = data[0]
            else:
                filebytes = data[0:datalength]
            #Alter data and adjust bytes and bytesize as bytes were not fully accepted
            data = data[self.bytesize:]
            self.bytesize -= datalength
            self.currentbytes += filebytes
        return data
    
    #Update each list with respective data
    def updateLists(self):
        self.namelist.append(self.currentname)
        self.bytelist.append(self.currentbytes)

    def resetData(self):
        self.currentname = ""
        self.currentbytes = ""