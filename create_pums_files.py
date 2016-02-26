import pandas as pd

hh_pums = pd.DataFrame.from_csv('Z:\Stefan\synthicity\psrc_synthpop\data\ss14hwa.csv', index_col = None)
p_pums = pd.DataFrame.from_csv('Z:\Stefan\synthicity\psrc_synthpop\data\ss14pwa.csv', index_col = None)


#data_set_list = {"puma00_p_%s_%s.csv" : p_pums, "puma10_h_%s_%s.csv"}
#cols = ['puma00', 'puma10']

    # get a list of unique ids for puma00 and puma10

df_2000_hh = hh_pums.loc[(hh_pums['PUMA00'] > 0)]
df_2000_pers = p_pums.loc[(p_pums['PUMA00'] > 0)]
id_list = list(set(df_2000_hh['PUMA00'].tolist()))
for id in id_list:
    hh_df = df_2000_hh.loc[(df_2000_hh['PUMA00'] == id)]
    pers_df = df_2000_pers.loc[(df_2000_pers['PUMA00'] == id)]
    
    if len(str(id))==4:
        id = '0%s' % (id)
    hh_df.to_csv(r'D:\Stefan\PopSynthesizer\PUMs2014\puma00_h_%s_%s.csv' % (53, id), index_col = False)
    pers_df.to_csv(r'D:\Stefan\PopSynthesizer\PUMs2014\puma00_p_%s_%s.csv' % (53, id), index_col = False)

df_2010_hh = hh_pums.loc[(hh_pums['PUMA10'] > 0)]
df_2010_pers = p_pums.loc[(p_pums['PUMA10'] > 0)]
id_list = list(set(df_2010_hh['PUMA10'].tolist()))
for id in id_list:
    hh_df = df_2010_hh.loc[(df_2010_hh['PUMA10'] == id)]
    pers_df = df_2010_pers.loc[(df_2010_pers['PUMA10'] == id)]
    
    if len(str(id))==4:
        id = '0%s' % (id)
    
    hh_df.to_csv(r'D:\Stefan\PopSynthesizer\PUMs2014\puma10_h_%s_%s.csv' % (53, id), index_col = False)
    pers_df.to_csv(r'D:\Stefan\PopSynthesizer\PUMs2014\puma10_p_%s_%s.csv' % (53, id), index_col = False)