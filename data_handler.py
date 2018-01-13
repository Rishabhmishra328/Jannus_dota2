import pandas as pd

class data_handler:
    
    def get_hero_features():
        hf_df = pd.read_csv('hero_features.csv', index_col=False)
        return(hf_df)

    def get_hero_features_with_id(id):
        hf_df = pd.read_csv('hero_features.csv', index_col=False)
        hf_df = hf_df.loc[hf_df['hid'] == id]
        hf_df = hf_df[['carry','support','nuker','disabler','jungler','durable','escape','pusher','initiator','class','attack']].astype('float32').values
        return(hf_df)

    print(get_hero_features_with_id(2))