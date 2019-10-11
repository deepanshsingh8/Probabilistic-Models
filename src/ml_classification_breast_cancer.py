'''
This is the task 4  which is done with ML classifiers (KNN, RFC)
Comments to be updated later
'''

from __future__ import division
from __future__ import print_function

# Necessary libraries
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

input_file = '../resources/bc_2.csv'

with open(input_file) as f:
    data = pd.read_csv(f)

print(data.head())
print(data.shape)

le = LabelEncoder()
for col in data.columns:
    data[col] = le.fit_transform(data[col])

print(data.head())

Y = data["BC"]
X = data.drop(["BC"], axis=1)
print(X.shape)

seed = 10
X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=0.2, random_state=seed)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

print(X_train.shape)

# K Nearest Neighbor
count = 0
nob = 15
neighbors = range(1, nob)
for neighbor in neighbors:
    knn = KNeighborsClassifier(n_neighbors=neighbor)
    knn.fit(X_train, Y_train)
    knn_score = round(knn.score(X_train, Y_train) * 100, 2)
    print('KNN Score for number of neighbors {} is {}: \n'.format(neighbor, knn_score))

    # Predict Output
    predicted = knn.predict(X_test)

    # Accuracy Score of KNN
    if neighbor > 10:
        a = accuracy_score(Y_test, predicted)
        if neighbor is 18:
            print("Classification Report :")
            print(classification_report(Y_test, predicted))
            conf2 = confusion_matrix(Y_test, predicted)
            print(conf2)
        count = count + a
        print('Accuracy Score for KNN with number of neighbors {} is {}: \n'.format(neighbor, a))
    else:
        print('Accuracy Score for KNN with number of neighbors {} is {}: \n'.format(neighbor,
                                                                                    accuracy_score(Y_test, predicted)))

print('The average accuracy is {}'.format((count / (nob - 10))))


# Random Forest
rf = RandomForestClassifier(max_depth=5, n_estimators=100, random_state=0)
rf.fit(X_train, Y_train)
print("Accuracy of Random Forest Classifier on training set: {:.3f}".format(rf.score(X_train, Y_train)))

predictions_rf = rf.predict(X_test)

# Accuracy Score of LG
print("Accuracy Score on prediction is:")
print(accuracy_score(Y_test, predictions_rf))
# Classification Report
print("Classification Report on RFC :")
print(classification_report(Y_test, predictions_rf))
conf5 = confusion_matrix(Y_test, predictions_rf)
print(conf5)
