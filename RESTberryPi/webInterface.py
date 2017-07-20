from flask import Flask, request
from rx import subjects

app = Flask(__name__, static_url_path='')
gpio_write_request = subjects.Subject()


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


def run():
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
