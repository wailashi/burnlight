import gevent
import itertools
from datetime import datetime, timedelta
import gpio


class Schedule(object):
    new_id = itertools.count().next

    def __init__(self, block, channels, start=datetime.utcnow()):
        self.id = Schedule.new_id()
        self.block = block
        self.channels = channels
        self.due = start
        self.active = True
        self._generator = self._start_generator()

    def _start_generator(self):
        for event in self.block.traverse():
            self.due = datetime.utcnow() + event.duration
            yield event

    def execute(self):
        try:
            next_event = next(self._generator)
            self.set_outputs(next_event.state)
        except StopIteration:
            self.active = False

    def set_outputs(self, state):
            print(str(datetime.utcnow()) + ': Channel ' + str(self.channels) + ' set to ' + state)
            for channel in self.channels.values():
                channel.set(state)


class Scheduler(object):

    def __init__(self):
        self.schedules = {}
        self._worker = gevent.Greenlet.spawn(self._worker)

    def _worker(self):
        while True:
            for schedule in self.schedules.values():
                if schedule.active and schedule.due < datetime.utcnow():
                    schedule.execute()
            gevent.sleep(1)

    def add_schedule(self, block, channels, start=datetime.utcnow()):
        channels = gpio.channels
        new_schedule = Schedule(block, channels, start)
        self.schedules[new_schedule.id] = new_schedule
        return new_schedule
