import time

import ioHandler
import webInterface


def gpio_write_request_handler(io, value):
    channel = int(value['channel'])
    string_state = value['state']
    string_state.upper()
    bool_state = False
    if state in ['ON', 'HIGH', '1']:
        bool_state = True
    elif state in ['OFF', 'LOW', '0']:
        bool_state = False
    io.set_channel(channel, bool_state)


# main application loop
if __name__ == '__main__':
    webInterface.run()
    io = ioHandler.IOHandler()
    io.setup_pins()
    subscription = webInterface.gpio_write_request.subscribe(
        on_next=lambda x: gpio_write_request_handler(io, x))
    counter = 0
    while True:
        time.sleep(0.05)
        for index in range(len(io.output_channels)):
            state = (counter & (2 ** index)) == 1
            io.set_channel(index, state)
        counter += 1
        counter %= 256
