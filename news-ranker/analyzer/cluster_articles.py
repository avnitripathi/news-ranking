import json

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer


def restructure_data():
    with open('../data/extracted_headlines.json') as f:
        data = json.load(f)
    headline_to_source = {}
    source_number = {}
    i = 0
    for k, v in data.items():
        for val in v:
            headline_to_source[val] = i
        source_number[k] = i
        i += 1
    return headline_to_source


restructured = restructure_data()


def encode_text(data):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data.keys())
    kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=100, n_init=1)
    kmeans.fit_predict(X)
    label = kmeans.labels_.tolist()

encode_text(restructured)