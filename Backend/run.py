import json
from finetune import Classifier
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    data = request.get_json()
    modelpath = '../Model/liar_BERT'
    model = Classifier.load(modelpath)
    predictions = model.predict(data['article'])
    print(predictions)
    if data['article'].find("propaganda") == -1:
        return jsonify({"bool": "0"})
    else:
        return jsonify({"bool": "1"})


if __name__ == '__main__':
    app.run(debug=True)
