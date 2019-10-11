from sklearn.metrics import accuracy_score
import src.conditional_probability_estimation as prob
import src.sampling as sampling
import pandas as pd
from collections import OrderedDict as odict

input_file = '../resources/bc_2.csv'

with open(input_file) as f:
    data = pd.read_csv(f)

# Dividing the train to 80 percent
train_split = 0.8
train_data = data.loc[0:data.shape[0] * train_split - 1, :]
test_data = data.loc[data.shape[0] * train_split:, :]
print(train_data.shape)
print(test_data.shape)

train_csv = train_data.to_csv('../resources/train.csv', index=None, header=True)

outcomeSpace, train_prob_tables = prob.learn_bayes_net(prob.graphT, 'train.csv')

queryNodes = list(outcomeSpace.keys())
train_p = sampling.p_joint(outcomeSpace, train_prob_tables, queryNodes)

prob.printFactor(train_prob_tables['BC'])

# Splitting
target = test_data["BC"]
test_X = test_data.drop(["BC"], axis=1)
test_evidence = odict()

# Bayesian Modelling
test_column = list(test_X.columns)
predictions = []
for i in range(test_X.shape[0]):
    for j in range(test_X.shape[1]):
        test_evidence[test_column[j]] = test_data.iloc[i][test_column[j]]
    row_probs = sampling.query(train_p, outcomeSpace, 'BC', test_evidence)
    all_probs_for_BC = row_probs['table']
    max_value = max(all_probs_for_BC, key=all_probs_for_BC.get)
    predictions.append(max_value[0])

print("Accuracy Score on prediction for Bayesian Network:")
print(accuracy_score(target, predictions))
