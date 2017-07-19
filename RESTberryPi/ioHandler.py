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
        GPIO.setup(self.output_channels, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.input_channels, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        for channel in self.input_channels:
            GPIO.add_event_detect(channel, GPIO.BOTH, callback=self.input_edge_callback, bouncetime=100)

    def input_edge_callback(self, pin):
        """callback to handle detected input edges
        :param pin: the number of the physical pin with detected edge
        """
        channel = self.input_channels.index(pin)
        self.input_states[channel] = GPIO.input(pin) == GPIO.HIGH

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

    def cleanup(self):
        """performs the cleanup of all pins"""
        GPIO.cleanup(self.output_channels)
        GPIO.cleanup(self.input_channels)
        self.input_states = [False] * 8
