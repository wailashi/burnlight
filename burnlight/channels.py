import logging
from datetime import datetime

log = logging.getLogger(__name__)


class Channel:

    def __init__(self, name, output_pin, input_pin=None):
        self.name = name
        self.state = None
        self.output_pin = output_pin
        if input_pin is not None:
            self.input_pin = input_pin

    def set(self, state):
        self.state = state
        log.info('Channel %s set to %s', self.name, state)

    @property
    def output(self):
        raise NotImplementedError

    @property
    def input(self):
        raise NotImplementedError

    def valid(self):
        if self.input_pin is None:
            return None
        else:
            return self.output == self.input

    def status(self):
        return {
            'state': self.state,
            'valid': self.valid(),
        }


class Dummy(Channel):

    def __init__(self, name, output_pin, input_pin=None):
        log.info('Init dummy channel %s' % name)
        Channel.__init__(self, name, output_pin, input_pin)

    def input(self):
        if self.input_pin is None:
            return None
        else:
            return self.state

    def output(self):
        return self.state

    def set(self, state):
        self.state = state
        print('{} Channel: \'{}\' set to {}'.format(datetime.utcnow(), self.name, state))
