import pandas as pd
from progress.bar import Bar
import numpy as np
import os

def get_hero_features():
    hf_df = pd.read_csv('./data/hero_features.csv', index_col=False)
    return(hf_df)

def get_hero_features_with_id(id):
    hf_df = pd.read_csv('./data/hero_features.csv', index_col=False)
    hf_df = hf_df.loc[hf_df['hid'] == id]
    hf_df = hf_df[['carry','support','nuker','disabler','jungler','durable','escape','pusher','initiator','class','attack']].astype('float32').values
    return(hf_df)

def get_data(ratio):
    test_data = []
    train_data = []
    if(ratio == None):
        with open('./data/test_data.npy', 'r') as test:
            test_data = np.load(test)
        with open('./data/train_data.npy', 'r') as train:
            train_data = np.load(train)

    else:
        p_df = pd.read_csv('./data/picks_data.csv', index_col=False)
        data = []
        m_pbar = Bar('Data Progress', max = len(p_df.values[:100]))
        for match in p_df.values[:100]:
            match_element = []
            m_pbar.next()
            for hero in match:
                h_features = get_hero_features_with_id(hero)
                match_element.append(h_features)
            data.append(match_element)
        data = np.asarray(data)
        train_len = int(round(len(data) * ratio))
        train_data = data[:train_len]
        test_data = data[train_len:]

        for index in range(len(train_data)):
            print(train_data[index])
            convert_to_one_hot(train_data[index])

        print(train_data[0], train_data[1])
        # print train_data[0],test_data[0]

        if not (os.path.isfile('./data/test_data.npy')):
            with open('./data/test_data.npy', 'w') as test_file:
                np.save(test_file, test_data)

        if not (os.path.isfile('./data/train_data.npy')):
            with open('./data/train_data.npy', 'w') as train_file:
                np.save(train_file, train_data)

    return train_data,test_data

def convert_to_one_hot(data):
    print(data)
    one_hot_vector = []
    for hero in data:
        for hval in hero:
            one_hot = []
            for val in hval:
                temp_data = [0.] * 4
                if(val == 0.):
                    temp_data = [1., 0., 0., 0.]
                if(val == 1.):
                    temp_data = [0., 1., 0., 0.]
                if(val == 2.):
                    temp_data = [0., 0., 1., 0,]
                if(val == 3.):
                    temp_data = [0., 0., 0., 1.]

                # np.concatenate(np.asarray(one_hot), np.asarray(temp_data))
                one_hot.append(temp_data)
                # val = int(val)
            one_hot = np.asarray(one_hot, dtype = np.float32).flatten()
            # print(hval, one_hot)
            one_hot_vector.append(one_hot)
    print(np.asarray(one_hot_vector))


get_data(ratio = 0.7)