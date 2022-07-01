import pandas as pd


def get_months_df(months):
    list = []
    for month in months:
        df = pd.read_csv(f'{month}.csv', sep=';')
        df.fillna(0, inplace=True)
        for column in df.columns[1:]:
            df[column] = df[column].astype(int)
        
        list.append(df)
    
    return list

months_of_year = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
df_months = get_months_df(months_of_year)

df_final = pd.concat(df_months).groupby(['Municípios']).sum().reset_index()
df_final.to_csv('2020.csv', sep=',', encoding='utf-8', index=False)