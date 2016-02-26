import pandas as pd
import numpy as np
import pickle

def weight_samples (df, level_names, totals_col):
    #get totals for this cat
    for level_name in level_names:
        orig_cols = df[level_name].columns
        print 'here!!!!!'
        df[level_name, level_name + '_total'] =  df[level_name].sum(1)
        if level_name == 'hh_size':
            df['hh_size', 'increase'] = df['hh_size', 'seven or more'] * .05
            print df['hh_size', 'increase']
            df['hh_size', 'seven or more'] = df['hh_size', 'seven or more'] + df['hh_size', 'increase'] 
            df['hh_size', 'hh_size_total'] = df['hh_size', 'hh_size_total'] + df['hh_size', 'increase'] 
            df['hh_size', 'increase'] = 0
            df  = df.drop('increase', axis = 1, level=1)
        # get the proportions for each category
        for col_name in orig_cols:
            df[level_name, col_name + '_p'] = df[level_name, col_name] /  df[level_name, level_name + '_total'] 
            df[level_name, col_name] = df[level_name, col_name + '_p'] * df['totals', totals_col]
            df[level_name, col_name] = df[level_name, col_name].fillna(0)
        # Drop the temp columns
        for col in df[level_name].columns:
            if col not in orig_cols:
                df = df.drop(col, axis = 1, level=1)
    df  = df.drop(totals_col, axis = 1, level=1)
    df = np.round(df, 0)
    return df
    











#b = test(a, 'age', 'total pop')
#        #a['age', 'test1'] = a['age'].sum(1)