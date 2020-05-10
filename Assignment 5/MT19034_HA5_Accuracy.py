# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 21:00:24 2019

@author: Dibyendu
"""

import pickle 

dbfile = open('Accuracy_doc2vec', 'rb')      
db = pickle.load(dbfile)
print()
print("Acuracy of the doc2vec model is ",db['Accuracy'])
dbfile = open('Accuracy_cosine', 'rb')      
db = pickle.load(dbfile)
print()
print("Acuracy of the cosine_similarity model is ",db['Accuracy'])
