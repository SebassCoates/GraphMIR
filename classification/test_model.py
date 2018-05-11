from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier 
from sklearn.model_selection import cross_val_score

import numpy as np

classicaldata = open('data_label_train_0.csv', 'r').read().split('\n')
crowdata = [row.split(',') for row in classicaldata]
crowdata.remove([''])

classicaltest = open('data_label_test_0.csv', 'r').read().split('\n')
crowtest = [row.split(',') for row in classicaltest]
crowtest.remove([''])

jazzdata = open('data_label_train_1.csv', 'r').read().split('\n')
jrowdata = [row.split(',') for row in jazzdata]
jrowdata.remove([''])

jazztest = open('data_label_test_1.csv', 'r').read().split('\n')
jrowtest = [row.split(',') for row in jazztest]
jrowtest.remove([''])

trainingdata = np.vstack((np.array(crowdata), np.array(jrowdata)))
num_features = np.shape(trainingdata)[1] - 1
features = trainingdata[:,0:num_features]
labels = trainingdata[:,num_features]

testdata = np.vstack((np.array(crowtest), np.array(jrowtest)))
testfeatures = testdata[:,0:num_features]
testlabels = testdata[:,num_features]

def print_accuracy(real, predicted):
    incorrect = 0
    for i, val in enumerate(real):
        if val == predicted[i]:
            incorrect +=1
    print('Test Accuracy: ' + str(incorrect / len(real)))

print('KNN:')
classifier = KNeighborsClassifier(3)
classifier.fit(features, labels)
print_accuracy(classifier.predict(testfeatures), testlabels)
print()

print('D Tree:')
classifier = tree.DecisionTreeClassifier(max_depth=num_features)
classifier.fit(features, labels)
print_accuracy(classifier.predict(testfeatures), testlabels)
print()

print('Adaboost:')
classifier = AdaBoostClassifier(n_estimators=25) 
classifier.fit(features, labels)
print_accuracy(classifier.predict(testfeatures), testlabels)
print()

print('Gradient Boosting:')
classifier = GradientBoostingClassifier(n_estimators=25) 
classifier.fit(features, labels)
print_accuracy(classifier.predict(testfeatures), testlabels)
