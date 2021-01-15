import json
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    sentence = request.get_json()

    if sentence.find("propaganda") == -1:
        return jsonify({"bool": "0"})
    else:
        return jsonify({"bool": "1"})


if __name__ == '__main__':
    app.run(debug=True)
