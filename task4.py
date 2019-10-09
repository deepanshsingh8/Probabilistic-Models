# Make division default to floating-point, saving confusion
from __future__ import division
from __future__ import print_function

# Necessary libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

input_file = 'resources/bc_2.csv'

with open(input_file) as f:
    data = pd.read_csv(f)

print(data.head())

le = LabelEncoder()
for col in data.columns:
    data[col] = le.fit_transform(data[col])

print(data.head())

