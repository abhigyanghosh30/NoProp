from typing import Optional
from finetune import Classifier
from fastapi import Request, FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.post('/')
async def hello_world(request: Request):
    data = await request.json()
    modelpath = '/home/masterg/Documents/8th Semester/Social Computing/NoProp/Model/liar_BERT'
    model = Classifier.load(modelpath)
    predictions = model.predict(data['article'])
    print(predictions)
    print(data['article'])
    return {"bool":str(predictions[0])}
