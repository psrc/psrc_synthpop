import pandas as pd
import pickle

##Persons
#file = open('D:/Stefan/synthpop_2014/p_acs_cat_33.pickle', "rb")
#person_marginals33 = pickle.load(file)
#file.close()


#file = open('D:/Stefan/synthpop_2014/p_acs_cat_53.pickle', "rb")
#person_marginals53 = pickle.load(file)
#file.close()

#file = open('D:/Stefan/synthpop_2014/p_acs_cat_61.pickle', "rb")
#person_marginals61 = pickle.load(file)
#file.close()


#file = open('D:/Stefan/synthpop_2014/p_acs_cat_35.pickle', "rb")
#person_marginals35 = pickle.load(file)
#file.close()

#person_marginals33.columns = person_marginals33.columns.droplevel()
#person_marginals53.columns = person_marginals53.columns.droplevel()
#person_marginals61.columns = person_marginals61.columns.droplevel()
#person_marginals35.columns = person_marginals35.columns.droplevel()
#a = [person_marginals33, person_marginals53, person_marginals61, person_marginals35]
#person_marginals = pd.concat(a)

#HHs
county_name_list = [35, 53, 61, 33]
file_location = 'D:/Stefan/synthpop_2014/'
hh_dfs = []
for county_name in county_name_list:
    file = open('%sh_acs_cat_%s.pickle' % (file_location, county_name), "rb")
    hh_marginals = pickle.load(file)
    hh_marginals.columns = hh_marginals.columns.droplevel()
    hh_dfs.append(hh_marginals)
    file.close()


#file = open('D:/Stefan/synthpop_2014/h_acs_cat_53.pickle', "rb")
#hh_marginals53 = pickle.load(file)
#file.close()

#file = open('D:/Stefan/synthpop_2014/h_acs_cat_61.pickle', "rb")
#hh_marginals61 = pickle.load(file)
#file.close()


#file = open('D:/Stefan/synthpop_2014/h_acs_cat_35.pickle', "rb")
#hh_marginals35 = pickle.load(file)
#file.close()

#hh_marginals33.columns = hh_marginals33.columns.droplevel()
#hh_marginals53.columns = hh_marginals53.columns.droplevel()
#hh_marginals61.columns = hh_marginals61.columns.droplevel()
#hh_marginals35.columns = hh_marginals35.columns.droplevel()
#b = [hh_marginals33, hh_marginals53, hh_marginals61, hh_marginals35]
hh_marginals = pd.concat(hh_dfs)
hh_marginals.reset_index(inplace = True)
hh_marginals.tract = hh_marginals.tract.astype('int64')
hh_marginals.state = hh_marginals.state.astype('int64')
hh_marginals.county = hh_marginals.county.astype('int64')
hh_marginals['block group'] = hh_marginals['block group'].astype('int64')

hh_marginals.set_index(['state', 'county', 'tract', 'block group'], inplace = True)
hh_marginals_hh_size = hh_marginals[['seven or more', 'six', 'five', 'four', 'three', 'two',]]

person_vars = ['race', 'school_enrollment']
hh_vars = ['cars', 'hh_size', 'family', 'income', 'cat_id', 'state', 'county', 'tract', 'block group']

#person_synth = pd.read_csv('D:/Stefan/synthpop_2014/people_region.csv')
hh_synth = pd.read_csv('D:/Stefan/synthpop_2014/households_region.csv')

hh_synth = hh_synth[[col for col in hh_synth.columns if col in hh_vars]] 
ct = pd.crosstab([hh_synth['state'], hh_synth['county'], hh_synth['tract'], hh_synth['block group']], hh_synth.hh_size)
#ct.reset_index(inplace =True)
ct = ct.merge(hh_marginals_hh_size, how ='left', left_index = True, right_index = True)

f = open(r'D:\Stefan\synthpop_2014\hh_size_ct.pickle', 'wb')
pickle.dump(ct, f)
f.close()