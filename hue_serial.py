import serial
import time

import hue

ARDUINO = '/dev/ttyACM0'


def read_serial(port=9600):
    ser = serial.Serial(ARDUINO, port)
    while True:
        try:
            r = str(ser.readline())
            print(r)
            if 'A' in r:
                hue.toggle_lights()
            elif '1' in r:
                hue.button_1()
            elif '2' in r:
                hue.button_2()
            elif '3' in r:
                hue.button_3()
            time.sleep(5)
        except KeyboardInterrupt:
            print('\n--- Script stopped ---')
            break


if __name__ == '__main__':
    read_serial()
