from __future__ import print_function
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
from sklearn import metrics

from sklearn.cluster import KMeans, MiniBatchKMeans, AffinityPropagation

import logging
import sys
from time import time

import numpy as np
import pandas as pd

data = open("clean9kcenters.txt", 'r').readlines()
dataset = []
data = np.array(data)
for x in data :
	dataset.append(x)

vectorizer = TfidfVectorizer(max_df=0.5, max_features=10000, min_df=2, stop_words='english', use_idf=True)
X = vectorizer.fit_transform(dataset)
print(X.shape)


km = AffinityPropagation(max_iter = 10000, verbose=True).fit(X)

f2 = open('./center9kclusters/centers.txt', 'a')
centers = km.cluster_centers_
terms = vectorizer.get_feature_names()
for i in range(centers.shape[0]):
        f2.write("Cluster %d:" % i)
        for ind in centers[i]:
		indi = [list(line.nonzero()[1]) for line in ind]
		for k in indi[0] :
			f2.write(' %s' % terms[k])
        f2.write("\n")


cluster_map = pd.DataFrame()

cluster_map['cluster'] = km.labels_

for x in range(centers.shape[0]) :
        f1 = open('./centerclusters/clust_' + str(x) + '.txt', 'a')
        y = cluster_map[cluster_map.cluster == x]['cluster'].index
        for n in y :
                f1.write(data[n])