import serial
import time

import hue

ARDUINO = '/dev/ttyACM0'


def read_serial(port=9600):
    ser = serial.Serial(ARDUINO, port)
    while True:
        try:
            try:
                r = str(ser.readline())
                print('Key press:', r[2])
            except serial.SerialException:
                print('Serial read failed')
                continue

            if 'A' in r:
                print('Toggling lights.')
                hue.toggle_lights()
            elif '1' in r:
                print('Scene 1...')
                hue.button_1()
            elif '2' in r:
                print('Scene 2...')
                hue.button_2()
            elif '3' in r:
                print('Scene 3...')
                hue.button_3()

            time.sleep(5)

        except KeyboardInterrupt:
            print('\n--- Script stopped ---')
            break


if __name__ == '__main__':
    read_serial()
