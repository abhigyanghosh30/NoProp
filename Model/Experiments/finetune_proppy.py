import os

import pandas as pd
import numpy as np

from finetune import Classifier
from finetune.base_models import BERT, BERTLarge, RoBERTa, RoBERTaLarge
from finetune.base_models.bert.model import BERTModelLargeCased
from sklearn.metrics import classification_report

data_loc = '/scratch/zubair/Datasets/Proppy/'

#@title Dataset loading from CSV
proppy_train_path = os.path.join(data_loc, 'proppy_1.0.train.tsv')
proppy_train = pd.read_csv(
    proppy_train_path, 
    sep='\t', 
    header=None
    )

proppy_dev_path = os.path.join(data_loc, 'proppy_1.0.dev.tsv')
proppy_dev = pd.read_csv(
    proppy_dev_path, 
    sep='\t', 
    header=None
    )
# proppy_train = proppy_train.sample(n=5000, random_state=42)
# proppy_dev = proppy_dev.sample(n=500, random_state=42)

#@title Feature selection
def change(x):
  if x == 1:
    return 1
  else:
    return 0
train_texts = list(proppy_train[0])
train_labels = list(map(change, list(proppy_train[14])))
dev_texts = list(proppy_dev[0])
dev_labels = list(map(change, list(proppy_dev[14])))

model_name = 'proppy_BERT'
model = Classifier(base_model=BERT, n_epochs=3)
model.fit(train_texts, train_labels)
model.save('/scratch/zubair/'+model_name)

# model = Classifier.load(model_name)
dev_labels_pred = model.predict(dev_texts)
print(classification_report(dev_labels, dev_labels_pred))
