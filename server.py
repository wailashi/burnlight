import logging
from configparser import SafeConfigParser 
from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify, make_response, request, abort
from scheduler import Scheduler
from block import Block
from serializer import CustomJSONDecoder, CustomJSONEncoder
from output import OutputController, DebugHandler

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

config = SafeConfigParser()
config.read('config.ini')

output_controller = OutputController()
DebugHandler(output_controller)
scheduler = Scheduler(output_controller)

app = Flask(__name__)
app.json_decoder = CustomJSONDecoder
app.json_encoder = CustomJSONEncoder
app.debug = True


@app.route('/')
def index():
    return "Hello World!"


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_found():
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    return jsonify({'schedules': scheduler.schedules})


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


port = config.getint('Server', 'port')
server = WSGIServer(('', port), app)
log.info('Burnlight server started on %s',server.address)
server.serve_forever()
