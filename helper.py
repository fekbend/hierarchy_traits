import pandas as pd


''' Standard Cross-Cultural Sample (SCCS) data '''
# Societies - Variables data
data_s = pd.read_csv('https://raw.githubusercontent.com/D-PLACE/dplace-data/master/datasets/SCCS/data.csv')

# Societies data
societies_s = pd.read_csv('https://raw.githubusercontent.com/D-PLACE/dplace-data/master/datasets/SCCS/societies.csv')

# Variables data
variables_s = pd.read_csv('https://raw.githubusercontent.com/D-PLACE/dplace-data/master/datasets/SCCS/variables.csv')

# Variable code data
codes_s = pd.read_csv('https://raw.githubusercontent.com/D-PLACE/dplace-data/master/datasets/SCCS/codes.csv')

# Filter relevant columns
data_s = data_s[['soc_id', 'var_id', 'code']]
societies_s = societies_s[['id', 'pref_name_for_society', 'glottocode']]
variables_s = variables_s[['id', 'title', 'definition', 'category']]
codes_s = codes_s[['var_id', 'code', 'description']]

# Rename columns for consistency
societies_s = societies_s.rename(columns={'id': 'soc_id'})
variables_s = variables_s.rename(columns={'id': 'var_id'})
codes_s = codes_s.rename(columns={'description': 'code_description'})

# Merge DataFrames
d_long_s = pd.merge(data_s, societies_s, on='soc_id', how='left')
d_long_s = pd.merge(d_long_s, variables_s, on='var_id', how='left')
d_long_s = pd.merge(d_long_s, codes_s, how='left')

# Filter relevant rows
d_long_s = d_long_s[d_long_s['var_id'].isin(['SCCS274',                                 # Slavery: type
                                       'SCCS322', 'SCCS323', 'SCCS324', 'SCCS325',      # Obedience (young & old, male & female)
                                       'SCCS302', 'SCCS303', 'SCCS304', 'SCCS305',      # Competitiveness
                                       'SCCS310', 'SCCS311', 'SCCS312', 'SCCS313'])]    # Achievement


''' Robert L. Carneiro's Dataset (6th edition) '''
# Societies - Variables data
data_c = pd.read_csv('https://raw.githubusercontent.com/D-PLACE/dplace-dataset-carneiro/main/cldf/data.csv')

# Societies data
societies_c = pd.read_csv('https://raw.githubusercontent.com/D-PLACE/dplace-dataset-carneiro/main/cldf/societies.csv')

# Variables data
variables_c = pd.read_csv('https://raw.githubusercontent.com/D-PLACE/dplace-dataset-carneiro/main/cldf/variables.csv')

# Variable code data
codes_c = pd.read_csv('https://raw.githubusercontent.com/D-PLACE/dplace-dataset-carneiro/main/cldf/codes.csv')

# Filter relevant columns
data_c = data_c[['Soc_ID', 'Var_ID', 'Value']]
societies_c = societies_c[['Name', 'Glottocode', 'ID']]
variables_c = variables_c[['ID', 'Name', 'Description', 'category']]
codes_c = codes_c[['Var_ID', 'Description', 'ord']]

# Rename columns for consistency
data_c = data_c.rename(columns={'Soc_ID': 'soc_id', 'Var_ID': 'var_id', 'Value': 'code'})
societies_c = societies_c.rename(columns={'Name': 'pref_name_for_society', 'Glottocode': 'glottocode', 'ID': 'soc_id'})
variables_c = variables_c.rename(columns={'ID': 'var_id', 'Name': 'title', 'Description': 'definition'})
codes_c = codes_c.rename(columns={'Var_ID': 'var_id', 'Description': 'code_description', 'ord': 'code'})

# Merge DataFrames
d_long_c = pd.merge(data_c, societies_c, on='soc_id', how='left')
d_long_c = pd.merge(d_long_c, variables_c, on='var_id', how='left')
d_long_c = pd.merge(d_long_c, codes_c, how='left')

# Filter relevant rows
d_long_c = d_long_c[d_long_c['var_id'].isin(['CARNEIRO_326'])] # (Semi)Divine ruler


''' Merge SCCS and Carneiro datasets (on glottocode) '''
# Long format
d_long = pd.concat([d_long_s, d_long_c], ignore_index=True).sort_values('glottocode')

# Long format: drop soc_id column & reorder columns 
d_long = d_long.drop(columns=['soc_id'])
new_order = ['glottocode', 'pref_name_for_society', 'title', 'definition', 'category', 'var_id', 'code', 'code_description']
d_long = d_long.reindex(columns=new_order)

# Wide format
d_wide = d_long[['glottocode', 'pref_name_for_society', 'title', 'code']]
d_wide = d_wide.pivot(index='glottocode', columns='title', values='code')

# Wide format: Create new columns for (mean male/female trait values (across all ages)) and mean trait values
# d_wide['Achievement: Avg Boy'] = d_wide[['Achievement: Early Boy', 'Achievement: Late Boy']].mean(axis=1)
# d_wide['Achievement: Avg Girl'] = d_wide[['Achievement: Early Girl', 'Achievement: Late Girl']].mean(axis=1)
# d_wide['Competitiveness: Avg Boy'] = d_wide[['Competitiveness: Early Boy', 'Competitiveness: Late Boy']].mean(axis=1)
# d_wide['Competitiveness: Avg Girl'] = d_wide[['Competitiveness: Early Girl', 'Competitiveness: Late Girl']].mean(axis=1)
# d_wide['Obedience: Avg Boy'] = d_wide[['Obedience: Early Boy', 'Obedience: Late Boy']].mean(axis=1)
# d_wide['Obedience: Avg Girl'] = d_wide[['Obedience: Early Girl', 'Obedience: Late Girl']].mean(axis=1)

d_wide['Achievement: Avg'] = d_wide[['Achievement: Early Boy', 'Achievement: Late Boy', 'Achievement: Early Girl', 'Achievement: Late Girl']].mean(axis=1)
d_wide['Competitiveness: Avg'] = d_wide[['Competitiveness: Early Boy', 'Competitiveness: Late Boy', 'Competitiveness: Early Girl', 'Competitiveness: Late Girl']].mean(axis=1)
d_wide['Obedience: Avg'] = d_wide[['Obedience: Early Boy', 'Obedience: Late Boy', 'Obedience: Early Girl', 'Obedience: Late Girl']].mean(axis=1)

# Wide format: Drop separated trait columns, keep only the average columns
d_wide = d_wide.drop(columns=['Achievement: Early Boy', 'Achievement: Early Girl', 'Achievement: Late Boy', 'Achievement: Late Girl', 
                              'Competitiveness: Early Boy', 'Competitiveness: Early Girl', 'Competitiveness: Late Boy', 'Competitiveness: Late Girl',
                              'Obedience: Early Boy', 'Obedience: Early Girl', 'Obedience: Late Boy', 'Obedience: Late Girl'])

# Wide format: Rename & reorder columns
d_wide = d_wide.rename(columns={'Slavery: type [Note, identical to EA070]': 'Slavery: type'})
new_order = ['Achievement: Avg', 'Competitiveness: Avg', 'Obedience: Avg',
             'Slavery: type', '(Semi)divine ruler']
d_wide = d_wide.reindex(columns=new_order)

# Save to CSV files
d_long.to_csv('d_long.csv', index=False, na_rep='NA')
d_wide.to_csv('d_wide.csv', na_rep='NA')