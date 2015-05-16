pins = {}


class Channel(object):
    def __init__(self, inputPin, outputPin):
        if inputPin not in pins:
            pins[inputPin] = 'input'
        if outputPin not in pins:
            pins[outputPin] = 'output'

        self.inputPin = inputPin
        self.outputPin = outputPin


def sentinel(channelGroup):
    pass


class ChannelGroup(object):
    def __init__(self, name):
        self.name = name
        self.channels = []

    def add_channel(self, inputPin, outputPin):
        self.channels.append(Channel(inputPin, outputPin))

    def set(self, state):
        self.state = state
        print 'Channel group  %s set to %s' % (self.name, state)
