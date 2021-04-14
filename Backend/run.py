from finetune import Classifier
from fastapi import Request, FastAPI
import pandas as pd

modelpath_liar = '/home/masterg/Documents/8th Semester/Social Computing/NoProp/Model/liar_BERT'
modelpath_prop = '/home/masterg/Documents/8th Semester/Social Computing/NoProp/Model/proppy_BERT'

model_liar = None
model_prop = None
df = None

app = FastAPI()


@app.on_event('startup')
async def startup_event():
    global model_liar
    model_liar = Classifier.load(modelpath_liar)
    global model_prop
    model_prop = Classifier.load(modelpath_prop)
    global df
    df = pd.read_csv('labels.csv')


def normalize_url(source):
    source = source.replace("http://", "")
    source = source.replace("https://", "")
    source = source.replace("www.", "")
    source = source.replace("/", "")
    return source


@app.post('/')
async def hello_world(request: Request):
    data = await request.json()
    res = {}
    try:
        res = df[df['source_url_normalized'] == normalize_url(
            data['source'])].to_dict('records')[0]
        res['valid'] = True
        predictions_prop = model_prop.predict(data['article'])
        predictions_liar = model_liar.predict(data['article'])
        print(predictions_liar, predictions_prop)
        res["prop"] = str(predictions_prop[0])
        res["liar"] = str(predictions_liar[0])
    except IndexError:
        print("source not in list")
        res = {"valid": False}
    return res
