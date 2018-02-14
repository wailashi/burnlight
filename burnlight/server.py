import logging
from configparser import ConfigParser
from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify, make_response, request, abort
from burnlight.scheduler import Scheduler
from burnlight.block import Block
from burnlight.serializer import CustomJSONDecoder, CustomJSONEncoder

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

config = ConfigParser()
config.read('config.ini')

scheduler = Scheduler(config)

app = Flask(__name__)
app.json_decoder = CustomJSONDecoder
app.json_encoder = CustomJSONEncoder
app.debug = True


@app.route('/')
def index():
    return "Burnlight LED controller."


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    return jsonify(scheduler.list_schedules())


@app.route('/api/schedules', methods=['POST'])
def create_schedule():
    if not request.get_json(force=True):
        print('Request has no JSON')
        abort(400)
    block = request.get_json()
    if not isinstance(block, Block):
        print('Not a valid Block object')
        abort(400)
    print('Adding schedule')
    schedule = scheduler.add_schedule(block)
    return jsonify({'schedule': schedule}), 201


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
    if payload['command'] == 'run':
        scheduler.start(schedule_id)
    elif payload['command'] == 'stop':
        scheduler.stop(schedule_id)
    return jsonify({'schedule': scheduler.schedules[schedule_id]}), 200

port = config.getint('Server', 'port')
server = WSGIServer(('', port), app)
log.info('Burnlight server started on %s', server.address)
server.serve_forever()
