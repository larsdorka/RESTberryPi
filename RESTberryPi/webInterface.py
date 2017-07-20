from flask import Flask, request
from rx import subjects, Observable
import json

app = Flask(__name__, static_url_path='')
gpio_write_request = subjects.Subject()
gpio_output_states = list()
gpio_input_states = list()


@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file("404.html"), 404


@app.route('/', methods=['GET'])
def send_index_page():
    return app.send_static_file("index.html")


@app.route('/api', methods=['GET'])
def send_api_doc():
    return app.send_static_file("api-doc/RESTberryPiApi.json")


@app.route('/api/gpioWrite/channel/<channel>/state/<state>', methods=['GET'])
def gpio_write(channel, state):
    gpio_write_request.on_next({'channel': channel, 'state': state})
    return "received and put in queue: channel {}, state {}".format(channel, state)


@app.route('/api/gpioWrite', methods=['GET'])
def gpio_write_with_params():
    channel = request.args.get('channel')
    state = request.args.get('state')
    gpio_write_request.on_next({'channel': channel, 'state': state})
    return "received and put in queue: channel {}, state {}".format(channel, state)


@app.route('/api/gpioReadAll', methods=['GET'])
def gpio_read_all():
    return json.dumps(gpio_output_states, indent=2)


def setup_output_state_observer(observable: Observable):
    observable.subscribe(on_next=output_state_observer_handler)


def output_state_observer_handler(value):
    global gpio_output_states
    gpio_output_states = value


def setup_input_state_observer(observable: Observable):
    observable.subscribe(on_next=input_state_observer_handler)


def input_state_observer_handler(value):
    global gpio_input_states
    gpio_input_states = value


def run():
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
