# intent classifier

import spacy
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os
from joblib import dump, load

def get_features(texts):
    features = []
    for text in texts:
        doc = nlp(text)
        features.append(doc.vector)
        
    return np.array(features)

def train(features, labels, test_size=0.25, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=test_size, random_state=random_state)
    clf.fit(X_train, y_train)
    
    dump(clf, model_filename)
    
    predictions = clf.predict(X_test)
    print(classification_report(y_test, predictions))
    
def predict(text):
    doc = nlp(text)
    feature = doc.vector
    feature_reshaped = np.array([feature])
    preds = clf.predict(feature_reshaped)
    return preds[0]
    
def load_training_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(' ')
            # 句子可能包含空格，标签位于最后
            sentence = ' '.join(parts[:-1])
            label = int(parts[-1])
        
            texts.append(sentence)
            labels.append(label)

nlp = spacy.load("zh_core_web_md")
clf = LinearSVC()
model_filename = './classifier.joblib'
file_path = './training_data.txt'
texts = []
labels = []

if os.path.exists(model_filename):
    clf = load(model_filename)
else:
    load_training_data(file_path)
    features = get_features(texts)
    train(features, labels)
    dump(clf, model_filename)



