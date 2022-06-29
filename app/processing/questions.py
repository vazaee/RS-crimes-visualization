from app.processing.utils import *


#Relação de crimes por mandato de governador
def crimes_by_governor():
    df_dict = get_years_data()

    years_tarso = [df_dict['2011'], df_dict['2012'], df_dict['2013'], df_dict['2014']]
    years_sartori = [df_dict['2015'], df_dict['2016'], df_dict['2017'], df_dict['2018']]
    years_leite = [df_dict['2019'], df_dict['2020'], df_dict['2021'], df_dict['2022']]
   
    sum_crimes_tarso = get_crimes(years_tarso)
    sum_crimes_sartori = get_crimes(years_sartori) 
    sum_crimes_leite = get_crimes(years_leite)

    tarso_crimes = pd.DataFrame({'Crime':sum_crimes_tarso.index, \
                                    'Total':sum_crimes_tarso.values,
                                    'Governo': 'Tarso Genro'})

    sartori_crimes = pd.DataFrame({'Crime':sum_crimes_sartori.index, \
                                    'Total':sum_crimes_sartori.values,
                                    'Governo': 'José Ivo Sartori'})

    leite_crimes = pd.DataFrame({'Crime':sum_crimes_leite.index, \
                                    'Total':sum_crimes_leite.values,
                                    'Governo': 'Eduardo Leite'})

    total = pd.concat([tarso_crimes, sartori_crimes, leite_crimes])
    return total

#Como os indicadores criminais se comportam ao longo do tempo?
def crimes_over_time():
    dt_years = crimes_over('year')
    dt_months = crimes_over('month')

    return [dt_years, dt_months]

def crimes_over(option):

    if(option == 'year'):
        df = get_years_data()
        df.pop('2018')
        df.pop('2019')
        df.pop('2020')
        df.pop('2021')
        df.pop('2022')
    else:
        df = get_month_data()
    
    lst = []

    for key, value in df.items():
        dt = value.sum()[1:]

        crimes = pd.DataFrame({'crime':dt.index, \
                                'total':dt.values,
                                option: key})
        lst.append(crimes)

    return pd.concat(lst)


#Padrão de crimes em relação aos municipios
def get_crimes_pattern(year, crime_types):
    df_index = pd.read_csv(f'app/static/dataset/municipios.csv', sep=';', encoding='utf-8')

    df = get_years_data()[year]
    df = df[crime_types]

    df['Total de crimes'] = df.sum(numeric_only=True, axis=1)
    df['index'] = df_index['id']

    return df

def get_year_city(cities, years):
    df_years = get_years_data()
    empty_df = pd.DataFrame({'Crime':["Homicídio Doloso","Homicídio Doloso de Trânsito","Furtos","Furto de Veículo","Roubos","Latrocínio","Roubo de Veículo","Extorsão","Extorsão Mediante Sequestro","Estelionato","Delitos Relacionados à Corrupção","Delitos Relacionados à Armas e Munições","Entorpecentes - Posse","Entorpecentes - Tráfico"], \
                                    'Total':[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                    'Municipio': 'Sem Dados'})
    # print("EMPTY: ", empty_df)
    if len(cities) == 0 or len(years) == 0:
        # print("TA DEVOLVENDO O EMPTY: ", empty_df)
        return empty_df
    new_df = {}
    for key, value in df_years.items():
        if key in years:
            new_df[key] = value[value['Municipio'].isin(cities)]

    out_df = new_df[list(new_df.keys())[0]]
    for key, value in new_df.items():
        if key == list(new_df.keys())[0]:
            continue
        out_df = out_df.add(value, fill_value=0)
    out_df['Municipio'] = new_df[list(new_df.keys())[0]]['Municipio']
    cities_crimes = []
    for index, row in out_df.iterrows():
        cities_crimes.append(pd.DataFrame({'Crime':list(out_df.columns.values)[1:], \
                                    'Total':get_crime_amount_as_list(row, list(out_df.columns.values)),
                                    'Municipio': row['Municipio']}))
    return pd.concat(cities_crimes)

def get_cities():
    return get_years_data()['2011']['Municipio'].to_numpy()

def get_crime_amount_as_list(df_row, col_names):
    crimes = []
    for col in col_names:
        if col == "Municipio":
            continue
        crimes.append(df_row[col])
    return(list(crimes))