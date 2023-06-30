import network
import socket
from time import sleep
import machine

ssid = "Truva"
password = "bizimevimiz"

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
    client_socket, client_address = sock.accept()
    print('Connected to client:', client_address)
    while True:
        unityData = client_socket.recv(1024)
        if unityData == "calibration_step_1":


try:
    ip = connect()
    sock = open_socket(ip)
    serve(sock)
except KeyboardInterrupt:
    machine.reset()
