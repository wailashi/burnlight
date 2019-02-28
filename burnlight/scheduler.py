import gevent
import logging
import itertools
from datetime import datetime
from burnlight.channels import Channel

log = logging.getLogger(__name__)


class Schedule:
    new_id = itertools.count()

    def __init__(self, program, channels):
        self.id = next(Schedule.new_id)
        self.program = program
        self.state = None
        if channels is None:
            self.channels = dict()
        else:
            self.channels = channels
        self.start = None
        self.running = False

    def run(self, when=None):
        if when is None:
            when = datetime.utcnow()
        self.start = when
        self.running = True

    def stop(self):
        self.running = False
        self.start = None

    def execute(self):
        if not self.running:
            log.warning('Trying to execute an inactive schedule %s', self.id)
            return
        if self.start + self.program.length <= datetime.utcnow():
            log.info('Schedule %s finished!', self.id)
            self.running = False
        else:
            state = self.program.state_at(datetime.utcnow() - self.start)
            if state is not self.state:
                self.state = state
                self.set_outputs(self.state)

    def set_outputs(self, state):
        for channel in self.channels:
            channel.set(state)

    def __repr__(self):
        return '<Schedule {}>'.format(self.id)


class Scheduler:

    def __init__(self, config):
        self.schedules = {}
        self._worker = gevent.Greenlet.spawn(self._worker)
        self._sentinel = gevent.Greenlet.spawn(self._sentinel)
        self.channels = {}
        self._init_channels(config)

    def _init_channels(self, config):
        for name, pins in config.items('Channels'):
            pin_out, pin_in = pins.split(',')
            self.channels[name] = Channel(name, pin_out.strip(), pin_in.strip())

    def _worker(self):
        logging.info('Worker starting.')
        while True:
            log.debug('Worker tick.')
            for schedule in self.schedules.values():
                if schedule.running:
                    schedule.execute()
            gevent.sleep(1)

    def _sentinel(self):
        logging.info('Sentinel starting.')
        while True:
            log.debug('Sentinel tick.')
            for schedule in self.schedules.values():
                for channel in schedule.channels:
                    if channel.valid() is False:
                        log.warning('Channel {} output is not valid!'.format(channel.name))
            gevent.sleep(5)

    def add_schedule(self, program):
        new_schedule = Schedule(program, list(self.channels.values()))
        log.info('Adding Schedule %s', new_schedule)
        self.schedules[new_schedule.id] = new_schedule
        new_schedule.run()
        return new_schedule

    def start(self, schedule_id, when=None):
        self.schedules[schedule_id].run(when)

    def stop(self, schedule_id):
        self.schedules[schedule_id].stop()

    def remove(self, schedule_id):
        self.schedules.pop(schedule_id)

    def list_schedules(self):
        schedules_list = {}
        for schedule_id, schedule in self.schedules.items():
            summary = {
                'start': schedule.start,
                'running': schedule.running,
                'length': schedule.program.length.total_seconds()
            }

            schedules_list[schedule_id] = summary
        return schedules_list

    def list_channels(self):
        return {
            name: c.status() for name, c in self.channels.items()
        }
