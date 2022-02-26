import pandas as pd

def print_peptides(df):
    for seq in df['sequence']:
        print(seq.upper())

data_directory = '/Volumes/GoogleDrive/My Drive/MHC libraries/Mass spec data 2022/'
data_file = data_directory + '20220223_Stability_TMT11_20220223/peptideExport.CS.1.csv'
tmt_file = data_directory + '20220223_Stability_TMT11_20220223/tmt.csv'

tmt_channels = pd.read_csv(tmt_file, sep=' ')
tmt_channels['channel'] = tmt_channels['channel'] + '_total'

df = pd.read_csv(data_file)
df['length'] = df['sequence'].str.len()
df = df[df['length'] < 12]

df_ecoli = df[df['species'].str.contains('ECOLI')]
df_library = df[df['species'].str.contains('HUMAN') | df['species'].str.contains('pHLA_library')]

print_peptides(df_library[df['length'] == 9])

df_tmt = df_library[tmt_channels['channel']].fillna(0)
df_tmt.columns = tmt_channels['name']
df_tmt.index = df_library['sequence']
df_tmt.div(df_tmt['Ctrl'], axis=0)

out_file = data_directory + '20220223_Stability_TMT11_20220223/peptideTMT.csv'
df_tmt.to_csv(out_file)

df_tmt = pd.read_csv(out_file)
df_tmt
