import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import PCA

hf_csv = pd.read_csv('./data/hero_features.csv', index_col=False)
hf_csv = hf_csv[['carry','support','nuker','disabler','jungler','durable','escape','pusher','initiator','class','attack']]

def plot_2D():
    data = hf_csv.values
    res = PCA(data)
    print(res)

plot_2D()

# print(hf_csv.values)
# print(hf_csv.var(axis=0, skipna=None, level=None, ddof=1, numeric_only=None))