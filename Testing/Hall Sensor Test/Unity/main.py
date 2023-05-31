import serial

def main():
    s = serial.Serial(port="COM7", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
    # s.flush()

    mes = s.read_until()
    print(mes.decode(), end="")


if __name__ == "__main__":
    while True:
        main()