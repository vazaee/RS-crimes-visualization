import pandas as pd

YEARS = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2019', '2020', '2021']
MONTHS = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
COLUMNS = ['Municipio', 'Homicidio Doloso', 'Furtos', 'Furto de Veiculo', 'Roubos', 'Latrocinio', 'Roubo de Veiculo', 'Estelionato', 
    'Delitos Relacionados a Armas e Municoes', 'Entorpecentes - Posse', 'Entorpecentes - Trafico']

dfs = {}
for month in MONTHS:
    dfs[month] = []

for month in MONTHS:
    for year in YEARS:
        sep = ','
        if year in ['2017', '2018', '2019', '2020', '2021', '2022']:
            sep = ';'
        df = pd.read_csv(f'{year}\\{month}.csv', sep=sep)
        df.fillna(0, inplace=True)
        for column in df.columns[1:]:
            df[column] = df[column].astype(int)
        df = df[COLUMNS]
        print(year, " - ", month)
        dfs[month].append(df)

dfs_final = {}
for month in MONTHS:
    dfs_final[month] = pd.concat(dfs[month]).groupby(['Municipio']).sum().reset_index()
    dfs_final[month].to_csv(f'{month}.csv', sep=',', encoding='utf-8', index=False)
        

