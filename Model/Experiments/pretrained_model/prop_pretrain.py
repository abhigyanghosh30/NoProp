import time
import os
import shutil
from tokenizers import ByteLevelBPETokenizer
from tokenizers.processors import BertProcessing
from transformers import RobertaConfig
from transformers import RobertaTokenizerFast
from transformers import RobertaForSequenceClassification
from transformers import SingleSentenceClassificationProcessor
import logging
from transformers import Trainer, TrainingArguments
import csv
import sys
import numpy as np
from typing import Callable, Dict
from transformers import EvalPrediction
from transformers import (glue_compute_metrics,glue_output_modes,
                         glue_tasks_num_labels,)
import pandas as pd

from sklearn.metrics import precision_recall_fscore_support, accuracy_score

csv.field_size_limit(sys.maxsize)
os.environ['WANDB_DISABLED'] = 'true'
# out_dir = "./prop_new_v0/"
out_dir = "./prop_v0/"


def build_compute_metrics_fn(task_name: str) -> Callable[[EvalPrediction], Dict]:
      def compute_metrics_fn(p: EvalPrediction):
          preds = np.argmax(p.predictions, axis=1)
          print("metrics", p.label_ids)
          return glue_compute_metrics("mrpc", preds, p.label_ids)

      return compute_metrics_fn


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


pretrain_file = 'prop01_label.csv'

print(pretrain_file, out_dir, flush=True)
pretrain_txt_file = 'prop01.txt'
print(pretrain_txt_file, flush=True)

"""## Train a tokenizer

Training a byte-level BPE(Byte-pair encoding tokenizer (the same as GPT-2), with the same special tokens as RoBERTa), rather than a WordPiece tokenizer like BERT, because it will start building its vocabulary from an alphabet of single bytes, so all words will be decomposable into tokens (no more `<unk>` tokens).
"""
start = time.time()
# Initialize a tokenizer
tokenizer = ByteLevelBPETokenizer()

# Customize training
tokenizer.train(files=pretrain_txt_file, vocab_size=50265, min_frequency=2, special_tokens=[
    "<s>",
    "<pad>",
    "</s>",
    "<unk>",
    "<mask>",
])

"""Now let's save files to disk"""
# if os.path.isdir(out_dir):
#     shutil.rmtree(out_dir)
os.makedirs(out_dir, exist_ok=True)
tokenizer.save_model(out_dir)

end = time.time()
print("Tokenizer", end - start, flush=True)
tokenizer = ByteLevelBPETokenizer(
    out_dir+"vocab.json",
    out_dir+"merges.txt",
)


tokenizer._tokenizer.post_processor = BertProcessing(
    ("</s>", tokenizer.token_to_id("</s>")),
    ("<s>", tokenizer.token_to_id("<s>")),
)
tokenizer.enable_truncation(max_length=512)


"""## Train a language model from scratch

"""


config = RobertaConfig(
    vocab_size=50265,
    max_position_embeddings=514,
    num_attention_heads=12,
    num_hidden_layers=6,
    type_vocab_size=1,
)

tokenizer = RobertaTokenizerFast.from_pretrained(out_dir,
                                    max_len=512, truncation=True)

"""As we are training from scratch, we only initialize from a config,
 not from an existing pretrained model or checkpoint.
"""
model = RobertaForSequenceClassification(config=config)
model.num_parameters()


logging.basicConfig(level=logging.ERROR)

# Commented out IPython magic to ensure Python compatibility.
start = time.time()
print(pretrain_file, flush=True)

# df = pd.read_csv(pretrain_file, sep="\t", names=["text", "label"])
# label_list = df['label'].values.tolist()
# # print("label_list", label_list)
# text_list = df['text'].values.tolist()
# for text1 in text_list:
#     if "\t" in text1:
#         print("tab in text", text1)
#     text1 = text1.replace("\t", " ")
#     text1 = text1.replace("\s+", " ")

# # print("text_list", text_list)
# df2 = pd.DataFrame({"label":label_list, "text":text_list})
# df2.reset_index(drop=True, inplace=True)
# print(df2.describe(), flush=True)
# print(df2.head(5))
# print("len_labels", len(label_list))
# print("len_texts", len(text_list))

# df1 =df.loc[df['label'] == 1]
# print(df1.describe(), flush=True)
# df2 =df.loc[df['label'] == 0]
# print(df2.describe(), flush=True)
# df = pd.concat([df2.iloc[0:4021], df1])
# # df = df2
# df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# print(df.describe(), flush=True)
# print(df['label'], flush=True)
# print("len labels", len(df['label']), flush=True)
# print(df['text'], flush=True)
# print("len text", len(df['text']), flush=True)
# print(df['label'].isnull().values.any(), "labels")
# print(df['text'].isnull().values.any(), "text")
# print(df['label'].isnull().sum(), "labels")
# print(df['text'].isnull().sum(), "text")
# df2=df2.iloc[0:8000]
# print(df.iloc[450:480], flush=True)
# print("from 475", df.iloc[475:478], flush=True)
# df2.to_csv("tmp2_pre_train_file.csv", sep ="\t", header=None, index=False)
# pretrain_file2="tmp2_pre_train_file.csv"
# print(pretrain_file2, flush=True)
# df3 = pd.read_csv(pretrain_file2, sep="\t", header=None)
# print(df3.describe(), flush=True)
# print("from file", df3.head(5), flush=True)

if pretrain_file != "prop_new.csv":
    dataproc = SingleSentenceClassificationProcessor.create_from_csv(pretrain_file,
                    split_name='\t',
                    column_label=0,
                    column_text=1,
                    column_id=None,
                    skip_first_row=False)
else:
    dataproc = SingleSentenceClassificationProcessor.create_from_csv(pretrain_file,
                    split_name='\t',
                    column_label=1,
                    column_text=0,
                    column_id=None,
                    skip_first_row=False)
dataset1 = dataproc.get_features(tokenizer, max_length=512)

end = time.time()
print("pretrain get fetaure extract done", end - start, flush=True)



"""### Finally, we are all set to initialize our Trainer"""

training_args = TrainingArguments(
    output_dir= out_dir,          # output directory
    num_train_epochs=3,              # total # of training epochs
    per_device_train_batch_size=16,  # batch size per device during training
    per_device_eval_batch_size=16,   # batch size for evaluation
    # warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    # logging_dir='./logs',            # directory for storing logs
    # save_steps=20000,
    save_total_limit=2,
    do_train=False,
    do_eval=True,
    evaluate_during_training=False,
)
# training_args = TrainingArguments(
#     output_dir=out_dir,
#     overwrite_output_dir=True,
#     num_train_epochs=3,
#     per_gpu_train_batch_size=16,
#     save_steps=500,
#     save_total_limit=2,
#     evaluate_during_training=False,
# )
len_dataset1 = len(dataset1)
# print(len_dataset1, len(df), flush = True)
# len_dataset1 = len(df)+1
# dataset1 = dataset1[:len_dataset1]
eval_idx = int(len(dataset1)*0.80)
print("eval_idx", eval_idx, flush=True)

trainer = Trainer(
    model=model,                        
    args=training_args,                  # training arguments, defined above
    train_dataset=dataset1,         # training dataset
    # eval_dataset=dataset1,            # evaluation dataset
    compute_metrics=compute_metrics,
    prediction_loss_only=False,
)

# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=dataset1[:eval_idx],
#     eval_dataset=dataset1[eval_idx:],
#     compute_metrics=build_compute_metrics_fn("mrpc"),
#     prediction_loss_only=False,
# )
start = time.time()
trainer.train()
end = time.time()
print("train", end - start, flush=True)
trainer.save_model(out_dir)
print("save model done", flush=True)
metrics = trainer.evaluate(dataset1[100:])
print(metrics)
