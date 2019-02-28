import logging
from gpiozero import DigitalOutputDevice, DigitalInputDevice, Device

log = logging.getLogger(__name__)


class Channel:

    def __init__(self, name, output_pin, input_pin=None):
        self.name = name
        self.state = None
        self.output_pin = output_pin
        if input_pin is not None:
            self.input_pin = input_pin
        self.output_device = DigitalOutputDevice(output_pin)
        if input_pin:
            self.input_device = DigitalInputDevice(input_pin)

    def set(self, state):
        """Sets the channel output"""
        self.state = state
        if state == 'On':
            self.output_device.on()
        elif state == 'Off':
            self.output_device.off()
        else:
            raise NotImplementedError
        log.info('Channel %s set to %s', self.name, state)

    def valid(self):
        """
        Checks if the channel output is valid

        Returns: True, if the output and input pin states match.
                 False, if they don't match.
                 None, if no input pin is defined.

        """
        if self.input_pin is None:
            return None
        else:
            return self.output_device.value == self.input_device.value

    def status(self):
        return {
            'state': self.state,
            'valid': self.valid(),
        }
