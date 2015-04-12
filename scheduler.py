import gevent


def output(outputs, state):
    print 'Outputs ' + ", ".join(map(str, outputs)) + ' set to ' + str(state)


class Scheduler(object):

    def __init__(self, outputs, name=""):
        self.outputs = outputs
        self.name = name
        self.threads = []
        self.block = None

    def clear(self):
        """Clear all scheduled events."""
        gevent.killall(self.threads)

    def schedule(self, block):
        """ Schedules the given block to run immediately."""
        self.clear()
        self.block = block
        delay = 0
        for event in block.traverse():
            self.threads.append(gevent.spawn_later(delay, output,
                                                   self.outputs, event.state))
            delay += event.duration

    def join(self):
        gevent.joinall(self.threads)

    def is_running(self):
        if self.threads:
            return True
        else:
            return False
