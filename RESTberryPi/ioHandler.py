from rx import subjects, Observable
import platform
if platform.system() == "Windows":
    import gpioMockup as GPIO
else:
    import RPi.GPIO as GPIO


class IOHandler:
    """class for reading and writing to IO hardware of the Raspberry Pi"""

    def __init__(self):
        """constructor"""
        self.output_channels = [11, 12, 13, 15, 16, 18, 22, 7]
        self.output_states = [False] * len(self.output_channels)
        self.output_states_observable = subjects.BehaviorSubject(self.output_states)
        self.input_channels = [37, 32, 36, 38]
        self.input_states = [False] * len(self.input_channels)
        self.input_states_observable = subjects.BehaviorSubject(self.input_states)
        self.write_observer = None

    def setup_pins(self):
        """initializes the input and output pins"""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.output_channels, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.input_channels, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        for channel in self.input_channels:
            GPIO.add_event_detect(channel, GPIO.BOTH, callback=self.input_edge_callback, bouncetime=100)

    def setup_write_observer(self, observable: Observable):
        """subscribes to an observable
        :param observable: an observable emitting GPIO write requests
        """
        self.write_observer = observable.subscribe(on_next=self.gpio_write_request_handler)

    def gpio_write_request_handler(self, value):
        channel = int(value['channel'])
        string_state = value['state']
        string_state = string_state.upper()
        bool_state = False
        if string_state in ['TRUE', 'ON', 'HIGH', '1']:
            bool_state = True
        elif string_state in ['FALSE', 'OFF', 'LOW', '0']:
            bool_state = False
        self.set_channel(channel, bool_state)

    def input_edge_callback(self, pin):
        """callback to handle detected input edges
        :param pin: the number of the physical pin with detected edge
        """
        channel = self.input_channels.index(pin)
        self.input_states[channel] = GPIO.input(pin) == GPIO.HIGH
        self.input_states_observable.on_next(self.input_states)

    def set_pin(self, pin, state):
        """sets an output based on the physical pin
        :param pin: the number of the physical pin to set
        :param state: the boolean state of the output to set
        """
        if pin in self.output_channels:
            if state is True:
                GPIO.output(pin, GPIO.HIGH)
            elif state is False:
                GPIO.output(pin, GPIO.LOW)
        self.read_all_output_channels()

    def set_channel(self, channel, state):
        """sets an output based on the channel defined in the output channel list
        :param channel: the index of the configured input pin to set
        :param state: the boolean state of the output to set
        """
        if channel < len(self.output_channels):
            if state is True:
                GPIO.output(self.output_channels[channel], GPIO.HIGH)
            if state is False:
                GPIO.output(self.output_channels[channel], GPIO.LOW)
        self.read_all_output_channels()

    def get_pin(self, pin):
        """reads an input data based on the physical pin
        :param pin: the number of the physical pin to read
        :return: the boolean state of the input
        """
        result = False
        if pin in self.input_channels:
            pin = self.input_channels.index(pin)
            result = self.input_states[pin]
        return result

    def get_channel(self, channel):
        """reads an input data based on the channel defined in the input channel list
        :param channel: the index of the configured input pin to read
        :return: the boolean state of the input
        """
        result = False
        if channel < len(self.input_channels):
            result = self.input_states[channel]
        return result

    def read_all_output_channels(self):
        """reads the state of all configured output channels and emits with observable"""
        for index in range(len(self.output_channels)):
            self.output_states[index] = GPIO.input(self.output_channels[index]) == GPIO.HIGH
        self.output_states_observable.on_next(self.output_states)

    def cleanup(self):
        """performs the cleanup of all pins"""
        GPIO.output(self.output_channels, GPIO.LOW)
        GPIO.cleanup(self.output_channels)
        GPIO.cleanup(self.input_channels)
        self.input_states = [False] * 8
