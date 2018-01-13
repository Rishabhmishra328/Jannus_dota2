import pandas as pd

hf_csv = pd.read_csv('hero_features.csv', index_col=False)
hf_csv = hf_csv[['carry','support','nuker','disabler','jungler','durable','escape','pusher','initiator','class','attack']]
# print(hf_csv)
print(hf_csv.var(axis=0, skipna=None, level=None, ddof=1, numeric_only=None))