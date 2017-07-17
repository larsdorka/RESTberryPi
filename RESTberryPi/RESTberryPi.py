import RPi.GPIO as GPIO
import time

pins_out = [8, 10, 12, 16, 18, 22, 24, 26]

# main application loop
if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    for index in range(len(pins_out)):
        GPIO.setup(pins_out[index], GPIO.OUT)
    counter = 0
    while True:
        time.sleep(0.05)
        for index in range(len(pins_out)):
            state = counter & (2 ** index)
            pin = pins_out[index]
            GPIO.output(pin, state)
        counter += 1
        counter %= 256
