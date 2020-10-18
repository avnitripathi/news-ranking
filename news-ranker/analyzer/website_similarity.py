import json
import tensorflow as tf
import itertools
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
    """messages1 and messages2 represent the encoded headlines from two news sources
    corr represents the correlation between the two
    - currently returns average correlation"""
    if np.array_equal(messages2, messages1):
        return 1
    corr = np.corrcoef(messages1, messages2)
    return np.average(corr)


def find_similarity(message1, message2):
    """represents messages as vectors which are used to calculate similarity"""
    total = 0
    embed1 = []
    embed2 = []
    for i in range(len(message1)):
        encoded = embed([message1[i]])
        embed1.append(encoded)
    for j in range(len(message2)):
        encoded = embed([message2[j]])
        embed2.append(encoded)
    for i in range(len(message1)):
        max = 0
        for j in range(len(message2)):
            sim = average_similarity(embed1[i], embed2[j])
            if sim > max:
                max = sim
        total += max
    return total/len(message1)


def show_plot(similarity_matrix, keys):
    sns.set(font_scale=1.2)
    g = sns.heatmap(
        similarity_matrix,
        xticklabels=keys,
        yticklabels=keys,
        vmin=0,
        vmax=1,
        cmap="YlOrRd")
    g.set_xticklabels(keys)
    g.set_title("Semantic Textual Similarity")
    plt.show()


def calc_all_similarities():
    with open('news-ranker/data/extracted_headlines.json') as f:
        data = json.load(f)
    keys = list(data.keys())
    similarity_matrix = np.zeros((len(keys), len(keys)))
    for i in range(len(keys)):
        for j in range(len(keys)):
            similarity_matrix[i][j] = find_similarity(data[keys[i]], data[keys[j]])
    show_plot(similarity_matrix, keys)
    cluster_similarities(keys, similarity_matrix)
    return similarity_matrix
def cluster_similarities(keys, similarity_matrix):
    keyList = keys.copy()
    clone = similarity_matrix.copy()
    print(clone)
    k = []
    while(len(keyList) > 0):
        x, y = np.where(clone == np.amax(clone))[0][0], np.where(clone == np.amax(clone))[1][0]
        clone[x][y] = 0
        key1, key2 = keys[x], keys[y]
        if key1 == key2:
            continue
        if key1 in keyList or key2 in keyList:
            found = False
            for i in k:
                if key1 in i:
                    i.append(key2)
                    keyList.remove(key2)
                    found = True
                elif key2 in i:
                    i.append(key1)
                    keyList.remove(key1)
                    found = True
            if not found:
                k.append([key1, key2])
                keyList.remove(key1)
                keyList.remove(key2)
    print(k)
similar = calc_all_similarities()
print(similar)
