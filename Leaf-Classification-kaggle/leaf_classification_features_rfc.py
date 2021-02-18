# -*- coding: utf-8 -*-
"""Leaf_Classification_Features.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mbEeaB1noWUCDP9YyQRujQ5AU3iUFLDI
"""

# leaf classification dataset from kaggle
# link: https://www.kaggle.com/c/leaf-classification

from google.colab import files
upload = files.upload()

!unzip leaf-classification.zip

!unzip images.zip
!unzip test.csv.zip
!unzip train.csv.zip

# Commented out IPython magic to ensure Python compatibility.
# Notebook imports

import os
import math
import numpy as np
import pandas as pd

from PIL import Image
import cv2
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# %matplotlib inline

plt.ion()

train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')

train_df.head()

test_df.head()

train_df.shape, test_df.shape

def load_images_from_dir(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            img = cv2.resize(img,(224,224))
            images.append(np.array(img))
    images = np.array(images)
    return images

img_dir = '/content/images'

images = load_images_from_dir(img_dir)

images.shape, images[3].shape

plt.imshow(images[3])

train_df['id'],test_df['id']

# label encoding

from sklearn.preprocessing import LabelEncoder

def encode_labels(train,test):
    encoder = LabelEncoder().fit(train.species)
    labels = encoder.transform(train.species)
    classes = list(encoder.classes_)
    test_ids = test.id

    train = train.drop(['species','id'],axis=1)
    test = test.drop(['id'],axis=1)

    return train, labels, test, test_ids, classes

X, y, test_df, test_ids, classes = encode_labels(train_df,test_df)

X.shape,y.shape,train_df.shape,test_df.shape

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,stratify=y)

X_train.shape, y_train.shape, X_test.shape, y_test.shape

# normalize data
from sklearn.preprocessing import normalize

X_train_norm = normalize(X_train)
X_test_norm = normalize(X_test)

# RandomForestClassifier to classify images into categories

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(criterion='entropy',
                               n_estimators=700,
                               min_samples_split=5,
                               min_samples_leaf=1,
                               max_features = "auto",
                               oob_score=True,
                               random_state=0,
                               n_jobs=-1)

model.fit(X_train_norm,y_train)

accuracy = model.score(X_test_norm,y_test)

print('Accuracy = '+str(accuracy))

!unzip sample_submission.csv.zip

sample_df = pd.read_csv('sample_submission.csv')

sample_df.head(1)

# saving predicted probabilites

result = model.predict_proba(normalize(test_df))


res_df = pd.DataFrame(result,columns=classes)
res_df.insert(0,'id',test_ids)
res_df.reset_index()

res_df.shape

res_df.head(1)

# saving res_df to a .csv file

res_df.to_csv('test_preds.csv',index=False)

print('File saved successfully !')

