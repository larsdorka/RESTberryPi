import time

import ioHandler

# main application loop
if __name__ == '__main__':
    io = ioHandler.IOHandler()

    counter = 0
    while True:
        time.sleep(0.05)
        for index in range(len(io.output_channels)):
            state = (counter & (2 ** index)) > 0
            io.set_channel(index, state)
        counter += 1
        counter %= 256
