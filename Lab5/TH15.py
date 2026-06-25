# TH15.py - Another Naive Bayes Example
from sklearn.naive_bayes import MultinomialNB
import numpy as np

# Training data
e1 = [2, 1, 2, 2, 2, 2]
e2 = [2, 2, 2, 1, 2, 2]
e3 = [1, 0, 2, 1, 2, 0]
e4 = [2, 0, 1, 1, 2, 1]

train_data = np.array([e1, e2, e3, e4])
labels = np.array(['yes', 'yes', 'no', 'no'])

# Test data
test = np.array([[2, 1, 2, 1, 2, 0]])

model = MultinomialNB(alpha=1)
model.fit(train_data, labels)

print('Probability of test:', model.predict_proba(test))
print('Predicted class:', model.predict(test)[0])