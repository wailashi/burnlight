import gevent
import itertools
from datetime import datetime, timedelta
from output import OutputController


class Schedule(object):
    new_id = next(itertools.count())

    def __init__(self, block, start=datetime.utcnow()):
        self.id = Schedule.new_id
        self.block = block
        self.due = start
        self.output_controller = None
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
            self.output_controller.update_outputs(1,state)


class Scheduler(object):

    def __init__(self, output_controller):
        self.schedules = {}
        self._worker = gevent.Greenlet.spawn(self._worker)
        self.output_controller = output_controller

    def _worker(self):
        while True:
            for schedule in self.schedules.values():
                if schedule.active and schedule.due < datetime.utcnow():
                    schedule.execute()
            gevent.sleep(1)

    def add_schedule(self, block, start=datetime.utcnow()):
        new_schedule = Schedule(block, start)
        new_schedule.output_controller = self.output_controller
        self.schedules[new_schedule.id] = new_schedule
        return new_schedule
