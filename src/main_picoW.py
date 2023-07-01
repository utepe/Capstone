import network
import socket
from time import sleep
from machine import Pin, reset
from enum import Enum
import json

from app import WBA_mode, calibration_mode, unity_mode

ssid = "Truva"
password = "bizimevimiz"

client_socket = None

# TODO: cahnge this pin number
WBA_pin = Pin(14, mode=Pin.IN, pull=Pin.PULL_UP)

class mode(Enum):
    IDLE = 0
    CALIBRATION = 1
    UNITY = 2
    WBA = 3

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    address = (ip, 80)
    sock = socket.socket()
    sock.bind(address)
    sock.listen()
    return sock

# first check if the glove is connected to WBA to enter that mode
# If the glove is not in WBA mode then accept the socket and handle the socket requests 
def serve(sock):
    global client_socket
    while True:
        # check if in WBA mode
        if WBA_pin.value(): # WBA mode
            WBA_mode.sendData()
        else:
            if client_socket is None:
                client_socket, client_address = sock.accept()
                print('Connected to client:', client_address)
            unityData = client_socket.recv(1024)
            # TODO: pass in client_socket to calibration_mode and unity_mode
            if unityData == "calibration":  # CALIBRATION mode
                calibration_mode.calibrate()
            elif unityData == "unityMode":  # UNITY mode
                unity_mode.sendData()
            else:   # IDLE mode
                pass
                
try:
    ip = connect()
    sock = open_socket(ip)
    serve(sock)
except KeyboardInterrupt:
    reset()
