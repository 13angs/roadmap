from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    NAME = os.getenv('NAME', 'K8s')
    response = {'message': f'Hello, {NAME}!'}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
