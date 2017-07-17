from flask import Flask, request

app = Flask(__name__)


@app.route('/api/gpio', methods=['GET'])
def set_gpio():
    pin = request.args.get('pin')
    value = request.args.get('value')
    print("pin " + pin + " set to " + value)
    return "pin " + pin + " set to " + value


if __name__ == '__main__':
    app.run(debug=True)
