import plotly.express as px
import numpy as np


def get_governor_figs(crimes_by_governor):    
    fig = px.bar(crimes_by_governor, x="Crime", y="Total", color="Governo",
                    hover_name="Governo",
                    labels={'Total':'Número de ocorrencias'},
                    barmode='group', height=750, log_y=True)
    
    return fig

def get_time_figs(months, years):
    fig1 = px.line(months, x="year", y="total", color='crime', markers=True,
        labels=dict(year="Ano", total="Número de ocorrencias", crime="Crime"), height=750)
    fig2 = px.line(years, x="month", y="total", color='crime', markers=True,
        labels=dict(month="Mês", total="Número de ocorrencias", crime="Crime"), height=750)
    
    return (fig1, fig2)

def get_choropleth_fig(crime_by_city, counties):
    crime_by_city['Log Total de crimes'] = np.log10(crime_by_city['Total de crimes'])
    crime_by_city.loc[crime_by_city['Log Total de crimes'] < 0, 'Log Total de crimes'] = 0

    fig = px.choropleth_mapbox(crime_by_city, geojson=counties, locations='index', color='Log Total de crimes',
                                range_color=(0, 5),
                                hover_data=['Municipio', 'Total de crimes'],
                                mapbox_style="open-street-map",
                                height=700,
                                color_continuous_scale = ["#ffffff" ,"#2196f3", "#4caf50", "#ffeb3b", "#ff9800", "#f44336", "#7f0000"],
                                zoom=6, center = {"lat": -30.4589615, "lon": -53.5902456},
                                labels={"Log Total de crimes" : "Nível Criminal"},
                                opacity=0.5)

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def get_bar_fig_cities(cities_years):
    fig = px.bar(
        cities_years, x="Crime", y="Total", color="Municipio", barmode='group', height=750,
        hover_name="Municipio", log_y=True,
        labels={'Total':'Número de ocorrencias'})

    return fig