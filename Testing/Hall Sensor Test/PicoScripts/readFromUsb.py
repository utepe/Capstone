import sys
import os
from usbBuffer import bufferSTDIN, getByteBuffer, getLineBuffer
from _thread import start_new_thread
from time import sleep_ms
input_msg = None
bufferSTDINthread = start_new_thread(bufferSTDIN, ())
while True:
    input_msg = getLineBuffer()
    if input_msg and 'unityClientMessage' in input_msg:
        print("recievedData: ", input_msg)
    else:
        print("message from pico")
    sleep_ms(10)