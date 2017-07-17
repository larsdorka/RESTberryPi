import time

import ioHandler

# main application loop
if __name__ == '__main__':
    ioHandler = ioHandler.IOHandler()
    ioHandler.setup_pins()
    counter = 0
    while True:
        time.sleep(0.05)
        for index in range(ioHandler.output_channels):
            state = (counter & (2 ** index)) == 1
            ioHandler.set_channel(index, state)
        counter += 1
        counter %= 256
