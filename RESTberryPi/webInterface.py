from flask import Flask, request
from rx import subjects

app = Flask(__name__)
gpio_write_request = subjects.Subject()


@app.route('/', methods=['GET'])
def send_index_page():
    return "API is running"


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


def run():
    app.run(debug=True, host='0.0.0.0')
