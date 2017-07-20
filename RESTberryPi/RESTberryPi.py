import ioHandler
import webInterface

# main application loop
if __name__ == '__main__':
    io = ioHandler.IOHandler()
    io.setup_pins()
    io.setup_observer(webInterface.gpio_write_request)
    try:
        webInterface.run()
    except KeyboardInterrupt:
        print("Exiting on KeyboardInterrupt...")
    finally:
        io.cleanup()
