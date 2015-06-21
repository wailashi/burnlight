from ConfigParser import SafeConfigParser
from gevent.wsgi import WSGIServer
from flask import Flask, jsonify, make_response, request, abort
from scheduler import Scheduler
from block import Block
from serializer import CustomJSONDecoder, CustomJSONEncoder

parser = SafeConfigParser()
parser.read('serverconfig.ini')

scheduler = Scheduler()

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
    schedule = scheduler.add_schedule(block, None)
    return jsonify({'schedule': schedule}), 201


port = parser.getint('Server', 'port')
server = WSGIServer(('', port), app)
server.serve_forever()
