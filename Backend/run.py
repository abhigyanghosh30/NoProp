from finetune import Classifier
from fastapi import Request, FastAPI
import pandas as pd

modelpath_liar = '/home/masterg/Documents/8th Semester/Social Computing/NoProp/Model/liar_BERT'
modelpath_prop = '/home/masterg/Documents/8th Semester/Social Computing/NoProp/Model/proppy_BERT'
model_liar = Classifier.load(modelpath_liar)
model_prop = Classifier.load(modelpath_prop)
df = pd.read_csv('labels.csv')

app = FastAPI()


@app.get('/sources')
async def sources(request: Request):
    data = await request.json()
    try:
        res = df[df['source_url'] == data['source']].to_dict('records')[0]
        res['valid'] = True
        return res
    except:
        return {"valid": False}


@app.post('/')
async def hello_world(request: Request):
    data = await request.json()
    predictions_prop = model_prop.predict(data['article'])
    predictions_liar = model_liar.predict(data['article'])
    print(predictions_liar, predictions_prop)
    return {"prop": str(predictions_prop[0]), "liar": str(predictions_liar[0])}
