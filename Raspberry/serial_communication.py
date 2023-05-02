import serial
import time
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        string = input("Send commands to Arduino (ON/OFF): ")
        ser.write(string.encode('utf-8'))
        time.sleep(0.1)
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
