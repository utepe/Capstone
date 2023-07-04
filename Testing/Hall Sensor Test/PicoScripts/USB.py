#
# USB serial communication for the Raspberry Pi Pico (RD2040) using the second RD2040
# thread/processor (written by Dorian Wiskow - Janaury 2021) 
#
from sys import stdin, exit
from _thread import start_new_thread
from utime import sleep
# 
# global variables to share between both threads/processors
# 
# bufferSize = 1024                 # size of circular buffer to allocate
# buffer = [' '] * bufferSize       # circuolar incomming USB serial data buffer (pre fill)
# bufferEcho = True                 # USB serial port echo incooming characters (True/False) 
# bufferNextIn, bufferNextOut = 0,0 # pointers to next in/out character in circualr buffer
# terminateThread = False           # tell 'bufferSTDIN' function to terminate (True/False)
#
# bufferSTDIN() function to execute in parallel on second Pico RD2040 thread/processor
#
class USB:
    bufferSize = 1024                 # size of circular buffer to allocate
    buffer = [' '] * bufferSize       # circuolar incomming USB serial data buffer (pre fill)
    bufferEcho = True                 # USB serial port echo incooming characters (True/False) 
    bufferNextIn, bufferNextOut = 0,0 # pointers to next in/out character in circualr buffer
    terminateThread = False           # tell 'bufferSTDIN' function to terminate (True/False)

    def __init__(self):
        pass

    def bufferSTDIN(self):
        while True:                                 # endless loop
            if self.terminateThread:                     # if requested by main thread ...
                break                               #    ... exit loop
            self.buffer[self.bufferNextIn] = stdin.read(1)    # wait for/store next byte from USB serial
            if self.bufferEcho:                          # if echo is True ...
                print(self.buffer[self.bufferNextIn], end='') #    ... output byte to USB serial
            self.bufferNextIn += 1                       # bump pointer
            if self.bufferNextIn == self.bufferSize:          # ... and wrap, if necessary
                self.bufferNextIn = 0
#
# instantiate second 'background' thread on RD2040 dual processor to monitor and buffer
# incomming data from 'stdin' over USB serial port using ‘bufferSTDIN‘ function (above)
#
# bufferSTDINthread = start_new_thread(bufferSTDIN, ())

#
# function to check if a byte is available in the buffer and if so, return it
#
    def getByteBuffer(self):
        
        if self.bufferNextOut == self.bufferNextIn:           # if no unclaimed byte in buffer ...
            return ''                               #    ... return a null string
        n = self.bufferNextOut                           # save current pointer
        self.bufferNextOut += 1                          # bump pointer
        if self.bufferNextOut == self.bufferSize:             #    ... wrap, if necessary
            self.bufferNextOut = 0
        return (self.buffer[n])                          # return byte from buffer

#
# function to check if a line is available in the buffer and if so return it
# otherwise return a null string
#
# NOTE 1: a line is one or more bytes with the last byte being LF (\x0a)
#      2: a line containing only a single LF byte will also return a null string
#
    def getLineBuffer(self):

        if self.bufferNextOut == self.bufferNextIn:           # if no unclaimed byte in buffer ...
            return ''                               #    ... RETURN a null string

        n = self.bufferNextOut                           # search for a LF in unclaimed bytes
        while n != self.bufferNextIn:
            if self.buffer[n] == '\x0a':                 # if a LF found ... 
                break                               #    ... exit loop ('n' pointing to LF)
            n += 1                                  # bump pointer
            if n == self.bufferSize:                     #    ... wrap, if necessary
                n = 0
        if (n == self.bufferNextIn):                     # if no LF found ...
                return ''                           #    ... RETURN a null string

        line = ''                                   # LF found in unclaimed bytes at pointer 'n'
        n += 1                                      # bump pointer past LF
        if n == self.bufferSize:                         #    ... wrap, if necessary
            n = 0

        while self.bufferNextOut != n:                   # BUILD line to RETURN until LF pointer 'n' hit
            
            if self.buffer[self.bufferNextOut] == '\x0d':     # if byte is CR
                self.bufferNextOut += 1                  #    bump pointer
                if self.bufferNextOut == self.bufferSize:     #    ... wrap, if necessary
                    self.bufferNextOut = 0
                continue                            #    ignore (strip) any CR (\x0d) bytes
            
            if self.buffer[self.bufferNextOut] == '\x0a':     # if current byte is LF ...
                self.bufferNextOut += 1                  #    bump pointer
                if self.bufferNextOut == self.bufferSize:     #    ... wrap, if necessary
                    self.bufferNextOut = 0
                break                               #    and exit loop, ignoring (i.e. strip) LF byte
            line = line + self.buffer[self.bufferNextOut]     # add byte to line
            self.bufferNextOut += 1                      # bump pointer
            if self.bufferNextOut == self.bufferSize:         #    wrap, if necessary
                self.bufferNextOut = 0
        return line                                 # RETURN unclaimed line of input