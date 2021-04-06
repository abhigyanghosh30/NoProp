from typing import Optional
from finetune import Classifier
from fastapi import Request, FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.post('/')
async def hello_world(request: Request):
    data = await request.json()
    modelpath_liar = '/home/masterg/Documents/8th Semester/Social Computing/NoProp/Model/liar_BERT'
    modelpath_prop = '/home/masterg/Documents/8th Semester/Social Computing/NoProp/Model/proppy_BERT'
    model_liar = Classifier.load(modelpath_liar)
    model_prop = Classifier.load(modelpath_prop)
    predictions_prop = model_prop.predict(data['article'])
    predictions_liar = model_liar.predict(data['article'])
    print(predictions_liar, predictions_prop)
    return {"prop": str(predictions_prop[0]), "liar": str(predictions_liar[0])}
