---
title: Basic Classifiers
author: Zubair Abid
linkcolor: blue
---

The objective is to take the data, push it through a `sentence_transformer`
(most likely `distilbert-base-nli-stsb-mean-tokens`), and then use it as our X,
y being the prediction we want to make. No fancy training here, just embedding +
sklearn classifier. 

**Objective**: It's a sanity check to ensure we are not going overkill with our
models.

# On the Proppy Dataset -- for Propaganda

Code is available on [this colab link].

**Sentence embedding**: `distilbert-base-nli-stsb-mean-tokens`, unless specified
otherwise.

## MLP

Initially, ran it with only `max_iter` set to 100, and got $0.96$ F1 on
detecting not-propaganda, but only $0.64$ for detecting propaganda.

Then, we ran a Grid Search with the following parameters:

```python
parameters = {
    'activation': ['identity', 'tanh', 'relu'],
    'solver': ['lbfgs', 'adam'], 
    'max_iter': [100, 200, 500, 1000], 
    'hidden_layer_sizes': [(100,), (50, 100, 50), (100, 50, 50, 100)], 
    }
```

As this was taking too long to run, we just run a for loop with all possible
iterations for a bit to see if it is worth the compute. Spoiler: it isn't.

From a quick check, it seems that `max_iter` should be over 100 and that neither
that nor `hidden_layer_sizes` changes much. WRT the `solver`, Adam seems to be
better, but only just. Nothing too special about `activation`.

## Random Forest

By far the worst performer. With `max_depth` set to 2, it got 0 propaganda hits.
Setting it to 5 increased that to 1. Setting it to None, we get a few more --
57 -- but that is an F1 of $0.15$

No Grid Search was done due to the futility of it all.

## SVM

With default settings, $0.96$ F1 on no-propaganda, and $0.60$ F1 on propaganda
[^svmtime]. Trying it with the `poly` kernel didn't change anything.

[^svmtime]: As an aside -- this took *so long*. I wrote from the start of the
document to this point before I got the results on default settings, and had
been whiling away time before that too.

## Takeaway

From the language alone, we don't get > 65% F1 score. Custom training loop will
probably benefit this.

[this colab link]: https://colab.research.google.com/drive/1qTCiywH1UXvopLCY83hoAI4M3xCyv9Jl#scrollTo=Sq79yswoD2XM
