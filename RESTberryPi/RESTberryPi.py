import time

import ioHandler
import webInterface


# main application loop
if __name__ == '__main__':
    webInterface.run()
    io = ioHandler.IOHandler()
    io.setup_pins(webInterface.gpio_write_request)

    counter = 0
    while True:
        time.sleep(0.05)
        for index in range(len(io.output_channels)):
            state = (counter & (2 ** index)) == 1
            io.set_channel(index, state)
        counter += 1
        counter %= 256
