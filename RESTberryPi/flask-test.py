from flask import Flask, request
from rx import subjects

app = Flask(__name__, static_url_path='')

subject = subjects.Subject()


@app.route('/', methods=['GET'])
def send_index_page():
    return app.send_static_file('index.html')


@app.route('/api/gpio', methods=['GET'])
def set_gpio():
    pin = request.args.get('pin')
    state = request.args.get('state')
    subject.on_next({'pin': pin, 'state': state})
    return "received and put in queue: pin {}, state {}".format(pin, state)


def pin_handler(value):
    pin = value['pin']
    state = value['state']
    print("pin " + pin + " set to " + state)


if __name__ == '__main__':
    subscription = subject.subscribe(on_next=lambda x: pin_handler(x))
    app.run(debug=True, host='0.0.0.0')
