import tensorflow as tf
import data_handler as dh

train_data, test_data =dh.get_data(ratio=None)

print(train_data[0], test_data[0])