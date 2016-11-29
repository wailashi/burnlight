import logging

log = logging.getLogger(__name__)


class Channel:

    def __init__(self, name, output_pin, input_pin=None):
        self.name = name
        self.input_pin = input_pin
        self.output_pin = output_pin

    def set(self, state):
        pass


class Dummy(Channel):

    def __init__(self, name, output_pin, input_pin=None):
        Channel.__init__(self, name, output_pin, input_pin)

    def set(self, state):
        print('{} set to {}'.format(self.name, state))
