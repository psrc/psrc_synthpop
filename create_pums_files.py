import pandas as pd
import numpy as np
import os

# This script prepares the PUMs file to be read by SynthPop- Creates indiviudal household and person files for each 2000 and 2010 PUM Geography.

# Location of the state wide PUMs file:
input_pums_dir = 'R:/SynthPop2014/data/'
output_dir = 'pums_data'



if not os.path.exists(output_dir):
        os.makedirs(output_dir)


hh_pums = pd.DataFrame.from_csv(input_pums_dir + 'ss14hwa.csv', index_col = None)
p_pums = pd.DataFrame.from_csv(input_pums_dir + 'ss14pwa.csv', index_col = None)

# PUMs Housholds do not have a good number of workers variable. Define is_worker in the person file and then sum up for each household. Then Join as a new
# variable to the househld file.  
p_pums['is_worker'] = np.where((p_pums.ESR == 1) | (p_pums.ESR == 2) | (p_pums.ESR == 4) | (p_pums.ESR == 5), 1, 0)
workers = pd.DataFrame(p_pums.groupby(['SERIALNO'])['is_worker'].sum())
workers.reset_index(inplace = True)
hh_pums = hh_pums.merge(workers, how ='left', on = ['SERIALNO'])
hh_pums = hh_pums.rename(columns = {'is_worker' : 'num_workers'})
hh_pums['num_workers'] = hh_pums['num_workers'].replace([np.NaN], np.nan)
hh_pums['num_workers']= hh_pums['num_workers'].fillna(0)
    
#Split out the 2000 geography from the PUMs file
df_2000_hh = hh_pums.loc[(hh_pums['PUMA00'] > 0)]
df_2000_pers = p_pums.loc[(p_pums['PUMA00'] > 0)]


id_list = list(set(df_2000_hh['PUMA00'].tolist()))
for id in id_list:
    hh_df = df_2000_hh.loc[(df_2000_hh['PUMA00'] == id)]
    pers_df = df_2000_pers.loc[(df_2000_pers['PUMA00'] == id)]
    
    if len(str(id))==4:
        id = '0%s' % (id)
    hh_df.to_csv(output_dir + '/' +'puma00_h_%s_%s.csv' % (53, id), index_col = False)
    pers_df.to_csv(output_dir + '/' +  'puma00_p_%s_%s.csv' % (53, id), index_col = False)

#Split out the 2010 geography from the PUMs file
df_2010_hh = hh_pums.loc[(hh_pums['PUMA10'] > 0)]
df_2010_pers = p_pums.loc[(p_pums['PUMA10'] > 0)]
id_list = list(set(df_2010_hh['PUMA10'].tolist()))
for id in id_list:
    hh_df = df_2010_hh.loc[(df_2010_hh['PUMA10'] == id)]
    pers_df = df_2010_pers.loc[(df_2010_pers['PUMA10'] == id)]
    
    if len(str(id))==4:
        id = '0%s' % (id)
    
    hh_df.to_csv(output_dir + '/' + 'puma10_h_%s_%s.csv' % (53, id), index_col = False)
    pers_df.to_csv(output_dir + '/' + 'puma10_p_%s_%s.csv' % (53, id), index_col = False)