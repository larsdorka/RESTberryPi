import RPi.GPIO as GPIO
import time

import ioHandler


# main application loop
if __name__ == '__main__':
    ioHandler = ioHandler.IOHandler()
    ioHandler.setup_pins()
    counter = 0
    while True:
        time.sleep(0.05)
        for index in range(len(pins_out)):
            state = counter & (2 ** index)
            pin = pins_out[index]
            GPIO.output(pin, state)
        counter += 1
        counter %= 256
