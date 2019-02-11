from burnlight.channels import Channel
import logging
import RPi.GPIO as gpio

log = logging.getLogger(__name__)


class RPiGPIO(Channel):

    def __init__(self, name, output_pin, input_pin=None):
        Channel.__init__(self, name, output_pin, input_pin)
        log.info('Init RPiGPIO channel %s' % name)
        gpio.setmode(gpio.BOARD)
        gpio.setup(output_pin, gpio.OUT)

    def set(self, state):
        Channel.set(self, state)
        if state == 'On':
            gpio.output(self.output_pin, gpio.HIGH)
        elif state == 'Off':
            gpio.output(self.output_pin, gpio.LOW)
        else:
            raise NotImplementedError
