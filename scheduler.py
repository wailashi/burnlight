import gevent
import logging
import itertools
from datetime import datetime
try:
    from rpigpio import RPiGPIO as Channel
except ImportError:
    from channels import Dummy as Channel

log = logging.getLogger(__name__)


class Schedule(object):
    new_id = itertools.count()

    def __init__(self, block, channels):
        self.id = next(Schedule.new_id)
        self.block = block
        if channels is None:
            self.channels = {}
        else:
            self.channels = channels
        self.start = None
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
        for each in self.channels:
            each.set(state)

    def __repr__(self):
        return '<Schedule {}>'.format(self.id)


class Scheduler(object):

    def __init__(self, config):
        self.schedules = {}
        self._worker = gevent.Greenlet.spawn(self._worker)
        self.channels = {}
        self._init_channels(config)

    def _init_channels(self, config):
        for name, pins in config.items('Channels'):
            pin_out, pin_in = map(int, pins.split(','))
            self.channels[name] = Channel(pin_out, pin_in)

    def _worker(self):
        while True:
            log.debug('Worker tick.')
            for schedule in self.schedules.values():
                if schedule.running:
                    schedule.execute()
            gevent.sleep(1)

    def add_schedule(self, block, channels=None):
        new_schedule = Schedule(block, channels)
        log.info('Adding Schedule %s', new_schedule)
        self.schedules[new_schedule.id] = new_schedule
        new_schedule.run()
        return new_schedule

    def start(self, schedule_id, when=datetime.utcnow()):
        self.schedules[schedule_id].run(when)

    def stop(self, schedule_id):
        self.schedules[schedule_id].stop()

    def remove(self, schedule_id):
        self.schedules.pop(schedule_id)
