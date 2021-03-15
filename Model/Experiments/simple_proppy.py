from simpletransformers.classification import ClassificationModel
from sklearn.model_selection import train_test_split
import pandas as pd
# import tensorflow.compat.v1 as tf
# import tensorflow_hub as hub
from datetime import datetime
import pickle
import pandas as pd
import sklearn
from sklearn.utils import shuffle
import os

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

train={'text':train_texts, 'label':train_labels}
train= pd.DataFrame(train)

test={'text':dev_texts, 'label':dev_labels}
test= pd.DataFrame(test)

model_type = "bert"
model_name = "bert-base-cased"

train_args = {
    "overwrite_output_dir": True,
    "max_seq_length": 100,
    "num_train_epochs": 8,
    "no_save":False,
    "evaluate_during_training_steps": 10000,
    "train_batch_size": 8,
    "eval_batch_size": 8, 
    # "config": {
    #     "output_hidden_states": True
    # }
}

def f1_macro(labels, preds):
    return sklearn.metrics.f1_score(labels, preds, average='macro')

def f1_weighted(labels, preds):
    return sklearn.metrics.f1_score(labels, preds, average='weighted')

def precisionscore(labels, preds):
    return sklearn.metrics.precision_score(labels, preds, average='weighted')

def recallscore(labels, preds):
    return sklearn.metrics.recall_score(labels, preds, average='weighted')

# Create a ClassificationModel
# model = ClassificationModel(model_type, model_name, num_labels=3, args={"reprocess_input_data": True, "overwrite_output_dir": True})
model = ClassificationModel(model_type, model_name, num_labels=3, args=train_args)

# Train the model
model.train_model(train, eval_df=test)
# model.train_model(train)

# # # Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(test, acc=sklearn.metrics.accuracy_score, f1weighted=f1_weighted, precision=precisionscore, recall=recallscore, f1macro=f1_macro)
print("Result: ",result)
