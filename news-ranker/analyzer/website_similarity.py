import json


import tensorflow as tf

import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
print ("module %s loaded" % module_url)


def embed(input):
  return model(input)


def plot_similarity(labels, features, rotation):
  corr = np.inner(features, features)
  sns.set(font_scale=1.2)
  g = sns.heatmap(
      corr,
      xticklabels=labels,
      yticklabels=labels,
      vmin=0,
      vmax=1,
      cmap="YlOrRd")
  g.set_xticklabels(labels, rotation=rotation)
  g.set_title("Semantic Textual Similarity")
  plt.show()
  import pdb
  pdb.set_trace()


def run_and_plot(messages_):
  message_embeddings_ = embed(messages_)
  plot_similarity(messages_, message_embeddings_, 90)


def average_similarity(messages1, messages2):
    running_sum = 0
    for i in range(len(messages1)):
        for j in range(len(messages2)):
            running_sum += cosine_similarity(np.array(messages1[i]).reshape(1, -1), np.array(messages2[j]).reshape(1, -1))
    return running_sumgit /(len(messages1) * len(messages2))


def find_similarity(message1, message2):
    message1_encoded = embed(message1)
    message2_encoded = embed(message2)
    return average_similarity(message1_encoded, message2_encoded)


def calc_all_similarities():
    with open('../data/extracted_headlines.json') as f:
        data = json.load(f)
