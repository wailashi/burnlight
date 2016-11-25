import gevent
import logging
import itertools
from datetime import datetime

log = logging.getLogger(__name__)


class Schedule(object):
    new_id = itertools.count()

    def __init__(self, block, start=datetime.utcnow()):
        self.id = next(Schedule.new_id)
        self.block = block
        self.start = start
        self.output_controller = None
        if start is not None:
            self.running = True
        else:
            self.running = False

    def execute(self):
        if self.start + self.block.length <= datetime.utcnow():
            log.info('Schedule %s finished!', self.id)
            self.running = False
        else:
            self.set_outputs(self.block.state_at_time(datetime.utcnow() - self.start))

    def set_outputs(self, state):
            self.output_controller.update_outputs(1, state)

    def __repr__(self):
        return '<Schedule {}>'.format(self.id)


class Scheduler(object):

    def __init__(self, output_controller):
        self.schedules = {}
        self._worker = gevent.Greenlet.spawn(self._worker)
        self.output_controller = output_controller

    def _worker(self):
        while True:
            log.debug('Worker tick.')
            for schedule in self.schedules.values():
                if schedule.running:
                    schedule.execute()
            gevent.sleep(1)

    def add_schedule(self, block, start=None):
        if start is None:
            start = datetime.utcnow()
        new_schedule = Schedule(block, start=start)
        log.info('Adding Schedule %s start %s', new_schedule, start)
        new_schedule.output_controller = self.output_controller
        self.schedules[new_schedule.id] = new_schedule
        return new_schedule
