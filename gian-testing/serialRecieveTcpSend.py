import serial
import socket

# Serial port configuration
serial_port = 'COM3'  # Replace with your serial port
baud_rate = 9600  # Replace with your baud rate

# TCP connection configuration
tcp_host = '192.168.1.115'  # Replace with the TCP server IP address
tcp_port = 25001  # Replace with the TCP server port

# Create a serial connection
ser = serial.Serial(serial_port, baud_rate)

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the TCP server
sock.connect((tcp_host, tcp_port))

try:
    while True:
        # Read data from the serial port
        data = ser.readline().decode().strip()
        
        # Send the data to the TCP server
        sock.sendall(data.encode())
        
        # Print the data for verification
        print('Sent:', data)
        
except KeyboardInterrupt:
    print('Program terminated by user')

finally:
    # Close the serial connection and TCP socket
    ser.close()
    sock.close()