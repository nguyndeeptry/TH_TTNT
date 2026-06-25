# TH14.py - Naive Bayes Classifier Example
from sklearn.naive_bayes import MultinomialNB
import numpy as np

# Training data from the example
e1 = [2, 1, 1, 0, 0, 0, 0, 0, 0]  # d1
e2 = [1, 1, 0, 1, 1, 0, 0, 0, 0]  # d2
e3 = [0, 1, 0, 0, 1, 1, 0, 0, 0]  # d3
e4 = [0, 1, 0, 0, 0, 0, 1, 1, 1]  # d4

train_data = np.array([e1, e2, e3, e4])
labels = np.array(['yes', 'yes', 'yes', 'no'])  # yes = B (Bắc), no = N (Nam)

# Test data d5
test = np.array([[2, 0, 0, 1, 0, 0, 0, 1, 0]])

# Train model with Laplace smoothing (alpha=1)
model = MultinomialNB(alpha=1)
model.fit(train_data, labels)

# Predict
print('Probability of test document:', model.predict_proba(test))
print('Predicted class:', model.predict(test)[0])