import RPi.GPIO as GPIO
import time

# main application loop
if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.OUT)
    LED = False
    while True:
        time.sleep(0.5)
        GPIO.output(3, LED)
        LED != LED
