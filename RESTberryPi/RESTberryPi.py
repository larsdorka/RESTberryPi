import ioHandler
import webInterface

# main application loop
if __name__ == '__main__':
    io = ioHandler.IOHandler()
    io.setup_pins()
    io.setup_write_observer(webInterface.gpio_write_request)
    webInterface.setup_output_state_observer(io.output_states_observable)
    webInterface.setup_input_state_observer(io.input_states_observable)
    try:
        webInterface.run()
    except KeyboardInterrupt:
        print("Exiting on KeyboardInterrupt...")
    finally:
        io.cleanup()
