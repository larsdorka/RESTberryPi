import RPi.GPIO as GPIO


class IOHandler:
    """class for reading and writing to IO hardware of the Raspberry Pi"""

    def __init__(self):
        """constructor"""
        self.output_channels = [12, 16, 18, 22, 32, 36, 38, 40]
        self.input_channels = [11, 13, 15, 29, 31, 33, 35, 37]
        self.input_states = [False] * 8

    def setup_pins(self):
        """initializes the input and output pins"""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.output_channels, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.input_channels, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.input_channels, GPIO.BOTH, callback=self.input_edge_callback, bouncetime=100)

    def input_edge_callback(self, channel):
        """callback to handle detected input edges"""
        pin = self.input_channels.index(channel)
        self.input_states[pin] = GPIO.input(pin) == GPIO.HIGH

    def set_channel(self, channel, state):
        """sets an output based on the physical pin"""
        if channel in self.output_channels:
            if state is True:
                GPIO.output(channel, GPIO.HIGH)
            elif state is False:
                GPIO.output(channel, GPIO.LOW)

    def set_pin(self, pin, state):
        """sets an output based on the channel defined in the output channel list"""
        if len(self.output_channels) > pin:
            if state is True:
                GPIO.output(self.output_channels[pin], GPIO.HIGH)
            if state is False:
                GPIO.output(self.output_channels[pin], GPIO.LOW)

    def get_channel(self, channel):
        """reads an input data based on the physical pin"""
        result = False
        if channel in self.input_channels:
            pin = self.input_channels.index(channel)
            result = self.input_states[pin]
        return result

    def get_pin(self, pin):
        """reads an input data based on the channel defined in the input channel list"""
        result = False
        if len(self.input_channels) > pin:
            result = self.input_states[pin]
        return result

    def cleanup(self):
        """performs the cleanup of all pins"""
        GPIO.cleanup(self.output_channels)
        GPIO.cleanup(self.input_channels)
        self.input_states = [False] * 8
