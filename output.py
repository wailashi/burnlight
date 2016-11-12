import itertools

class OutputController:

    def __init__(self):
        self.__output_handlers = []
        self.channels = {}

    def init_settings(self, config):
        for each in config('Channels'):
            name, pins = each
            out_pin, in_pin = map(int, pins.split(','))
            self.add_channel(Channel(out_pin, in_pin))

    def register_output_handler(self, output_handler):
        self.__output_handlers.append(output_handler)

    def update_outputs(self, channel, state):
        for handler in self.__output_handlers:
            handler.update(channel, state)

    def add_channel(self, channel):
        self.channels[channel.number] = channel
        for handler in self.__output_handlers:
            handler.add_channel(channel)

class DebugHandler:
    def __init__(self, output_controller):
        output_controller.register_output_handler(self)

    def update(self, channel, state):
        print('Channel {} set to {}'.format(channel, state))

    def add_channel(self, channel):
        print('Added channel {}'.format(channel))

class Channel:
    new_channel_number = itertools.count()

    def __init__(self, output_pin, input_pin = None):
        self.input_pin = input_pin
        self.output_pin = output_pin
        self.number = next(self.new_channel_number)
        self.state = None

    def update(self, state):
        self.state = state

    def __repr__(self):
        return '<Channel {}, state {}>'.format(self.channel, self.state)
