# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.utils import shuffle
from sklearn.metrics import f1_score
import pickle
import time
import csv
import tensorflow as tf
import os
import sys
from glob import glob
from transformers import SingleSentenceClassificationProcessor
from sklearn.model_selection import train_test_split
import logging
from transformers import RobertaForSequenceClassification, RobertaTokenizer, Trainer, TrainingArguments
import numpy as np
from typing import Callable, Dict, Optional

from transformers import RobertaForSequenceClassification, RobertaTokenizer
from transformers import Trainer, TrainingArguments, EvalPrediction
from transformers import (glue_compute_metrics,glue_output_modes,
                         glue_tasks_num_labels,)

from sklearn.metrics import precision_recall_fscore_support, accuracy_score


csv.field_size_limit(sys.maxsize)
os.environ['WANDB_DISABLED'] = 'true'
train_data = 'liar_train.csv'
valid_data = 'liar_valid.csv'
model_dir = "./prop_v0"
tokenizer_dir = "./prop_v0"

out_dir = './results_train_sc6'
# train_data = 'training_1000.csv'

print(train_data, flush=True)
print(valid_data, flush=True)

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }
def clean_spaces(f_name):
    df = pd.read_csv(f_name, sep="\t", names=["label", "text"])
    label_list = df['label'].values.tolist()
    # print("label_list", label_list)
    text_list = df['text'].values.tolist()
    for text1 in text_list:
        if "\t" in text1:
            print("tab in text", text1)
        text1 = text1.replace("\t", " ")
        text1 = text1.replace("\s+", " ")
    df.to_csv("cleaned_"+f_name, sep ="\t", header=None, index=False)
    print(df.describe(), flush=True)
    print(df.head(5))

def get_dataset_from_file(fname, tokenizer):
    # clean_spaces(fname)
    # tmpfile = "cleaned_"+fname
    tmpfile = fname
    print("get_dataset_from_file", tmpfile, flush=True)
    start = time.time()
    dataproc = SingleSentenceClassificationProcessor.create_from_csv(tmpfile,
                    split_name='\t',
                    column_label=0,
                    column_text=1,
                    column_id=None,
                    skip_first_row=False)
    dataset = dataproc.get_features(tokenizer, max_length=512)
    end = time.time()        
    print(fname, len(dataset), flush=True)
    return dataset

#model = RobertaForSequenceClassification.from_pretrained(model_dir)
#tokenizer = RobertaTokenizer.from_pretrained(tokenizer_dir)

tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaForSequenceClassification.from_pretrained('roberta-base')

logging.basicConfig(level=logging.ERROR)

start_t = time.time()

train_dataset = get_dataset_from_file(train_data, tokenizer)
valid_dataset = get_dataset_from_file(valid_data, tokenizer)


end_t = time.time()
print("train  valid total extract feature complete", end_t - start_t, flush=True)
print(len(train_dataset), len(valid_dataset), flush=True)

training_args = TrainingArguments(
    output_dir=out_dir,          # output directory
    num_train_epochs=5 ,              # total # of training epochs
    per_device_train_batch_size=8,  # batch size per device during training
    per_device_eval_batch_size=8,   # batch size for evaluation
    # warmup_steps=500,                # number of warmup steps for learning rate scheduler
    # weight_decay=0.01,               # strength of weight decay
    # logging_dir='./logs',            # directory for storing logs
    # save_steps=20000,
    save_total_limit=2,
    do_train=True,
    do_eval=True,
    evaluate_during_training=False,
)

trainer = Trainer(
    model=model,                         # the instantiated 🤗 Transformers model to be trained
    args=training_args,                  # training arguments, defined above
    train_dataset=train_dataset,         # training dataset
    compute_metrics=compute_metrics,
    prediction_loss_only=False,
)

start = time.time()
trainer.train()
trainer.save_model(out_dir)
print("finsihed Training", flush=True)
metrics = trainer.evaluate(valid_dataset)
print(metrics, flush=True)
end = time.time()
print("Train Evaluate", end - start, flush=True)


