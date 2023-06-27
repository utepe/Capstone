from machine import UART
from time import sleep

# Set up the UART connection
uart = UART(0, baudrate=9600)  # Replace 0 with the appropriate UART number and baud rate

while True:
    if uart.any():
        # Read the data from UART
        recievedData = uart.read().decode('utf-8')
        if recievedData and "unityClientMessage" == recievedData:
            print("recievedData: ", recievedData)

        # Process the received data
        print("message from pico")
        sleep(0.2)
        # Add your desired logic here

# Close the UART connection (optional)
uart.deinit()