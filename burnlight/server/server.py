import logging
from pathlib import Path
from configparser import ConfigParser
from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify, make_response, request, abort
from burnlight.scheduler import Scheduler
from burnlight.programparser import loadBSL

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

config = ConfigParser()
config_path = Path('~/.config/burnlight/config.ini').expanduser()
if not config_path.is_file():
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config['Server'] = {'port': 34455}
    config['Channels'] = {
        'Channel 1': 'GPIO7, GPIO3',
        'Channel 2': 'GPIO11, GPI012',
        'Channel 3': 'GPIO13, GPIO15',
        'Channel 4': 'GPIO16, GPIO18',
        'Channel 5': 'GPIO19, GPIO20',
    }
    config.write(open(config_path, 'w'))
else:
    config.read(config_path)

scheduler = Scheduler(config)

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return "Burnlight LED controller."


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(e):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    return jsonify(scheduler.list_schedules())


@app.route('/api/schedules', methods=['POST'])
def create_schedule():
    if not request.get_json(force=True):
        print('Request has no JSON')
        abort(400)
    bsl = request.get_json()['program']
    program = loadBSL(bsl)
    schedule = scheduler.add_schedule(program)
    return jsonify({'schedule': program.to_bsl()}), 201


@app.route('/api/channels', methods=['GET'])
def list_channels():
    return jsonify(scheduler.list_channels())


@app.route('/api/schedules/<int:schedule_id>', methods=['GET', 'DELETE'])
def get_schedule(schedule_id):
    if request.method == 'GET':
        log.debug('GET schedule %s', schedule_id)
    elif request.method == 'DELETE':
        log.debug('DELETE schedule %s', schedule_id)


@app.route('/api/schedules/<int:schedule_id>', methods=['PATCH'])
def patch_schedule(schedule_id):
    if not request.get_json(force=True):
        print('Request has no JSON')
        abort(400)
    payload = request.get_json()
    if payload['command'] == 'start':
        scheduler.start(schedule_id)
    elif payload['command'] == 'stop':
        scheduler.stop(schedule_id)
    return '', 200


def main():

    port = config.getint('Server', 'port')
    server = WSGIServer(('', port), app)
    log.info('Burnlight server started on %s', server.address)
    server.serve_forever()
