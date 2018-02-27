import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelBinarizer

# Plotting scoring parameters
def plotting_fig(possible_estimators, accuracy, recall, precision, n_of_tests):    
    plt.figure(figsize = (13, 7))
    plt.plot(possible_estimators, accuracy)
    plt.xlabel("n_estimators")
    plt.ylabel("accuracy")
    plt.xticks(possible_estimators)
    plt.savefig("../Prezentacija/graphs/" + str(n_of_tests) + "_accuracy",  dpi = 100)
    plt.figure(figsize = (13, 7))
    plt.plot(possible_estimators, recall)
    plt.xlabel("n_estimators")
    plt.ylabel("recall")
    plt.xticks(possible_estimators)
    plt.savefig("../Prezentacija/graphs/" + str(n_of_tests) + "_recall",  dpi = 100)
    plt.figure(figsize = (13, 7))
    plt.plot(possible_estimators, recall)
    plt.xlabel("n_estimators")
    plt.ylabel("precision")
    plt.xticks(possible_estimators)
    plt.savefig("../Prezentacija/graphs/" + str(n_of_tests) + "_precision",  dpi = 100)

# Reading data, selecting values from all blood tests
df = pd.read_excel('Input.xlsx')
column_names = list(df)
column_names.pop()
X = df.ix[:, 'WBC':'CEA'].values
y = df.ix[:, 'Disease'].values

# Binarizing labels
lb = LabelBinarizer()
y = np.array([number[0] for number in lb.fit_transform(y)])

# Declaring variables and arrays
accuracy, recall, precision, result = [], [], [], []
i_begin = 10
i_end = 301
step = 10
best_result = pd.DataFrame(columns=['Data', 'Best Score', 'Accuracy', 'Recall', 'Precision']) 

# Number of trees that are going to be used in cross validation 
possible_estimators = np.arange(i_begin, i_end, step)

# Model evaluation by cross validation 
for i in xrange(i_begin, i_end, step):
    clf = RandomForestClassifier(n_estimators = i)    
    accuracy.append(cross_val_score(clf, X, y, cv = 10, scoring = 'accuracy').mean())
    recall.append(cross_val_score(clf, X, y, cv = 10, scoring = 'recall').mean())
    precision.append(cross_val_score(clf, X, y, cv = 10, scoring = 'precision').mean())
    print "1. run: " + str(i) + " estimators"

# Plotting scoring parameters
plotting_fig(possible_estimators, accuracy, recall, precision, 32)

# Calculating the best mean score for each number of trees
for i in range(0, len(accuracy)):
    result.append((recall[i] + accuracy[i] + precision[i]) / 3)

# Setting the best result for selected blood tests
best_result.set_value(0, 'Data', column_names)
best_result.set_value(0, 'Best Score', max(result))
best_result.set_value(0, 'Accuracy', accuracy[result.index(max(result))])
best_result.set_value(0, 'Recall', recall[result.index(max(result))]) 
best_result.set_value(0, 'Precision', precision[result.index(max(result))])

# Choosing the most efficient number of trees
num_of_estimators = possible_estimators[result.index(max(result))]
print "Selected number of estimators: " + str(num_of_estimators)

# Fitting the model with selected number of trees
clf = RandomForestClassifier(n_estimators = num_of_estimators)
clf.fit(X, y)

# Sorting the most important features
feature_importn = sorted(zip(column_names, clf.feature_importances_), key=lambda tup: tup[1], reverse = True)

# Cross validation for N important features
for i in [20, 10, 5, 2]:    
    if i == 20:
        k = 1
    elif i == 10:
        k = 2
    elif i == 5:
        k = 3
    else:
        k = 4
    # Selecting first N important features
    first_N_features = feature_importn[0:i]
    # Resetting column_names
    column_names = []
    for j in range(0, len(first_N_features)):
        column_names.append(first_N_features[j][0])
    
    # Selecting new input for cross validation
    temp_array = np.empty((119, 1))
    for element in first_N_features:
        x = df.ix[:, element[0]].values[:, np.newaxis]
        temp_array = np.hstack((temp_array, x))
    # Delete first column of zeroes    
    X = np.delete(temp_array, 0, 1)
    
    accuracy, recall, precision, result = [], [], [], []
    # Model evaluation by cross validation 
    for l in xrange(i_begin, i_end, step):
        clf1 = RandomForestClassifier(n_estimators = l)    
        accuracy.append(cross_val_score(clf1, X, y, cv = 10, scoring = 'accuracy').mean())
        recall.append(cross_val_score(clf1, X, y, cv = 10, scoring = 'recall').mean())
        precision.append(cross_val_score(clf1, X, y, cv = 10, scoring = 'precision').mean())
        print  str(k + 1) + ". run: " + str(l) + " estimators"
    
    # Plotting data
    plotting_fig(possible_estimators, accuracy, recall, precision, i)
    
    # Calculating the best result
    for m in range(0, len(accuracy)):
        result.append((recall[m] + accuracy[m] + precision[m]) / 3)    

    # Setting the best result for selected blood tests
    best_result.set_value(k, 'Data', column_names)
    best_result.set_value(k, 'Best Score', max(result))
    best_result.set_value(k, 'Accuracy', accuracy[result.index(max(result))])
    best_result.set_value(k, 'Recall', recall[result.index(max(result))])
    best_result.set_value(k, 'Precision', precision[result.index(max(result))])

# Writing to Excel
writer = pd.ExcelWriter('../Prezentacija/Output.xlsx')
best_result.to_excel(writer, 'Sheet1')
writer.save()