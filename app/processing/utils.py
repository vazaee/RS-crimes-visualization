import pandas as pd
import json

from urllib.request import urlopen


MONTHS = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho',
        'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

CRIMES = ['Homicidio Doloso', 'Homicidio Doloso de Transito', 'Furtos', 
    'Furto de Veiculo', 'Roubos', 'Latrocinio', 'Roubo de Veiculo', 'Extorsao', 'Extorsao Mediante Sequestro', 'Estelionato', 
    'Delitos Relacionados a Corrupcao', 'Delitos Relacionados a Armas e Municoes', 'Entorpecentes - Posse', 'Entorpecentes - Trafico']

YEARS = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']

COLUMNS_EQUALS = ['Municipio', 'Homicidio Doloso', 'Furtos', 'Furto de Veiculo', 'Roubos', 'Latrocinio', 'Roubo de Veiculo', 'Estelionato', 
    'Delitos Relacionados a Armas e Municoes', 'Entorpecentes - Posse', 'Entorpecentes - Trafico']

def get_years_data():
    df_years = {}
    for year in range(2011, 2023):
        df = pd.read_csv(f'app/static/dataset/dataset-by-year/{year}.csv', sep=',', encoding='utf-8')
        df = df[COLUMNS_EQUALS]
        df_years[str(year)] = df
    
    return df_years

def get_month_data():
    return {month : pd.read_csv(f'app/static/dataset/dataset-by-month/{month}.csv', sep=',', encoding='utf-8') \
          for month in MONTHS}

def get_crimes(years):
    years = [year[COLUMNS_EQUALS] for year in years]
    df = pd.concat(years).groupby(['Municipio']).sum().reset_index()
    
    only_values = df.drop(['Municipio'], axis=1)
    crimes_sum = only_values.sum(axis=0)

    return crimes_sum.sort_values(ascending=False)

def get_geo_json():
    counties = []
    with urlopen('https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-43-mun.json') as response:
        counties = edit_json(json.load(response))

    return counties

def edit_json(json):
    for feature in json['features']:
        feature['id'] = feature['properties']['id']

    return json