from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier 
from sklearn.model_selection import cross_val_score

import numpy as np

classicaldata = open('data_label=0.csv', 'r').read().split('\n')
crowdata = [row.split(',') for row in classicaldata]
crowdata.remove([''])
crowdata = np.array(crowdata)[0:100,:]

jazzdata = open('data_label=1.csv', 'r').read().split('\n')
jrowdata = [row.split(',') for row in jazzdata]
jrowdata.remove([''])
jrowdata = np.array(jrowdata)[0:100,:]

trainingdata = np.vstack((np.array(crowdata), np.array(jrowdata)))
num_features = np.shape(trainingdata)[1] - 1
features = trainingdata[:,0:num_features]
labels = trainingdata[:,num_features]

print("Testing KNN, 10-Fold CV")
Ks = [1, 3, 5, 7, 9, 13, 21, 49, 101]
for K in Ks:
    classifier = KNeighborsClassifier(K)
    scores = cross_val_score(classifier, features, labels, cv=10)
    print("Error: %0.3f (+/- %0.3f) for k=%d" % (1 - scores.mean(), scores.std() * 2, K))
print()

print("Testing Decision Tree")
depths = [i + 1 for i in range((num_features))]
for depth in depths:
    classifier = tree.DecisionTreeClassifier(max_depth=depth)
    scores = cross_val_score(classifier, features, labels, cv=10)
    print("Error: %0.3f (+/- %0.3f) for depth=%d" % (1 - scores.mean(), scores.std() * 2, depth))
print()

print("Adaboosting")
numEstimators = [i for i in range(1,50, 2)]
for num in numEstimators:
    classifier = AdaBoostClassifier(n_estimators=num) 
    scores = cross_val_score(classifier, features, labels, cv=10)
    print("Error: %0.3f (+/- %0.3f) for num_estimators=%d" % (1 - scores.mean(), scores.std() * 2, num))
print()

print("Gradient Boosting")
numEstimators = [i for i in range(1, 50, 2)]
for num in numEstimators:
    classifier = GradientBoostingClassifier(n_estimators=num) 
    scores = cross_val_score(classifier, features, labels, cv=10)
    print("Error: %0.3f (+/- %0.3f) for num_estimators=%d" % (1 - scores.mean(), scores.std() * 2, num))
print()
