import ioHandler
import webInterface

# main application loop
if __name__ == '__main__':
    io = ioHandler.IOHandler()
    io.setup_pins()
    io.setup_observer(webInterface.gpio_write_request)
    webInterface.run()
