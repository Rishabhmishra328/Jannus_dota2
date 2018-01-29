import tensorflow as tf
import data_handler as dh
import numpy as np

train_data, test_data =dh.get_data(ratio=None)

train_x = np.asarray([val[:5] for val in train_data])
train_y = np.asarray([val[5:] for val in train_data])

test_x = np.asarray([val[:5] for val in test_data])
test_y = np.asarray([val[5:] for val in test_data])


def first_pick_model():
    pass

print train_x[0],test_x[0],train_y[0],test_y[0]
