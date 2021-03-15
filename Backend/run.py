import json
from finetune import Classifier
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    data = request.get_json()
    modelpath = '/home/masterg/Documents/8th Semester/Social Computing/NoProp/Model/liar_BERT'
    model = Classifier.load(modelpath)
    predictions = model.predict(data['article'])
    print(predictions)
    print(data['article'])
    return jsonify({"bool":str(predictions[0])})

if __name__ == '__main__':
    app.run(debug=True)
