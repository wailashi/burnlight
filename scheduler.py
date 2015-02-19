import gevent
from datetime import datetime, timedelta


class Schedule(object):

    def __init__(self, block, io_bank, start=datetime.utcnow()):
        self.block = block
        self.io_bank = io_bank
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
            print(datetime.utcnow() + ': IO bank ' + io_bank + ' set to ' + next_event.state)
        except StopIteration:
            self.active = False


class Scheduler(object):

    def __init__(self):
        self.schedules = []
        self.worker = gevent.Greenlet.spawn(self._worker)


    def _worker(self):
        while True:
            for schedule in self.schedules:
                if schedule.active and schedule.due < datetime.utcnow():
                    schedule.execute()
            gevent.sleep(1)


    def add_schedule(self, block, io_bank, start=datetime.utcnow()):
        self.schedules.append(Schedule(block, io_bank, start))
