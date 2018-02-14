from burnlight.channels import Channel
import RPi.GPIO as gpio


class RPiGPIO(Channel):

    def __init__(self, name, output_pin, input_pin=None):
        Channel.__init__(self, name, output_pin, input_pin)
        gpio.setmode(gpio.BOARD)
        gpio.setup(output_pin, gpio.OUT)

    def set(self, state):
        Channel.set(self, state)
        if state == 'HIGH':
            gpio.output(self.output_pin, gpio.HIGH)
        elif state == 'LOW':
            gpio.output(self.output_pin, gpio.LOW)
        else:
            raise NotImplementedError
