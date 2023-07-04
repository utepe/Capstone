import serial
import socket

# Serial port configuration
serial_port = 'COM3'  # Replace with your serial port
baud_rate = 9600  # Replace with your baud rate

# TCP connection configuration
host = 'localhost'  # Replace with the TCP server IP address
port = 25001  # Replace with the TCP server port

# Create a serial connection
ser = serial.Serial(serial_port, baud_rate)

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the TCP server
sock.bind((host, port))
sock.listen()

print('Server is listening on {}:{}'.format(host, port))

# Accept a client connection
client_socket, client_address = sock.accept()
print('Connected to client:', client_address)

try:
    while True:
        # Receive data from the client
        clientData = client_socket.recv(1024).decode('utf-8')
        print('Client received data:', clientData)

        # Read data from the serial port
        ser.write(clientData.encode('utf-8'))
        
        # Send a response to the client
        response = "Data coming from the serial port"
        client_socket.send(response.encode('utf-8'))
        print('Sent:', response)
        
        serialData = ser.readline().decode().strip()
        print('Received data from serial port:', serialData)
        
except KeyboardInterrupt:
    print('Program terminated by user')

finally:
    # Close the serial connection and TCP socket
    # ser.close()
    sock.close()