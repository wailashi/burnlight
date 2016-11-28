import gevent
import logging
import itertools
from datetime import datetime

log = logging.getLogger(__name__)


class Schedule(object):
    new_id = itertools.count()

    def __init__(self, block):
        self.id = next(Schedule.new_id)
        self.block = block
        self.start = None
        self.output_controller = None
        self.running = False

    def run(self, when=datetime.utcnow()):
        self.start = when
        self.running = True

    def stop(self):
        self.running = False
        self.start = None

    def execute(self):
        if not self.running:
            log.warning('Trying to execute a inactive schedule %s', self.id)
            return
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

    def add_schedule(self, block):
        new_schedule = Schedule(block)
        log.info('Adding Schedule %s', new_schedule)
        new_schedule.output_controller = self.output_controller
        self.schedules[new_schedule.id] = new_schedule
        new_schedule.run()
        return new_schedule

    def start(self, schedule_id, when=datetime.utcnow()):
        self.schedules[schedule_id].run(when)

    def stop(self, schedule_id):
        self.schedules[schedule_id].stop()

    def remove(self, schedule_id):
        self.schedules.pop(schedule_id)
