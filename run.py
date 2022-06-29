from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from app.processing.figures_gen import *
from app.processing.questions import *
from app.processing.utils import YEARS, CRIMES


df_by_governor = crimes_by_governor()
over_time = crimes_over_time()   
    
fig1, fig2 = get_first_figs(df_by_governor)
fig3, fig4 = get_time_figs(*over_time)

CITIES = get_cities()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "CrimeRS"

app.layout = html.Div([

    dbc.NavbarSimple(
        brand="CrimeRS - Dashboard Criminal do Rio Grande do Sul",
        brand_href="#",
        color="#212529",
        dark=True,
    ),

    html.Div([
        # html.H1(children="CrimeRS"),
    
        #html.Div([
        #    html.H2(children='Relação de crimes por mandato de governador'),
        #    dcc.Graph(figure=fig1),
        #]),

        #html.Div([
        #    html.H2(children='Relação de crimes por mandato de governador normalizado'),
        #    dcc.Graph(figure=fig2),
        #]),
        
        dbc.Card(
            html.Div([
                html.H2(children='Indicadores Criminais ao longo dos anos'),
                dcc.Graph(figure=fig3),
            ]),
            style={'padding':'20px 50px', 'margin-bottom':20}
        ),

        dbc.Card(
            html.Div([
                html.H2(children='Indicadores Criminais ao longo dos meses (anos acumulados 2011-2016)'),
                dcc.Graph(figure=fig4),
            ]),
            style={'padding':'20px 50px', 'margin-bottom':20}
        ),

        dbc.Card(
            html.Div([
                html.H2("Indicadores Criminais por Município"),
                
                html.Div([
                    dcc.Dropdown(
                        CITIES,
                        ['PORTO ALEGRE'],
                        id='dropdown-city',
                        multi=True,
                        placeholder="Insira o nome de uma ou mais cidades"
                    )
                ],style={'width':'70%', 'margin-top':20, 'margin-bottom':15}),

                dcc.Checklist(
                    id='checkbox-year',                      # used to identify component in callback
                    options=[
                        {'label': year, 'value': year, 'disabled':False}
                        for year in YEARS
                    ],
                    value=YEARS,
                    className='checkbox-year',
                    inputClassName='checkbox-year-input',
                    inputStyle={'cursor': 'pointer'},
                    labelClassName='checkbox-crime-label',
                    labelStyle={'margin-right': '0.5rem'},
                ), 

                dcc.Graph(id='bar-city')
            ]),
            style={'padding':'20px 50px', 'margin-bottom':20}
        ),

        dbc.Card(
            html.Div([
                html.H2("Mapa Criminal do Rio Grande do Sul"),
                dcc.Checklist(
                    id='checkbox-crime',                      # used to identify component in callback
                    options=[
                        {'label': crime, 'value': crime, 'disabled':False}
                        for crime in CRIMES
                    ],
                    value=CRIMES,
                    className='checkbox-crime',
                    inputClassName='checkbox-crime-input',
                    inputStyle={'cursor': 'pointer'},
                    labelClassName='checkbox-crime-label',
                    labelStyle={'margin-right': '0.5rem'},
                ),
                dcc.Dropdown(YEARS, YEARS[len(YEARS)-1], id='dropdown-year', style={'margin-top': 15}, clearable=False, searchable=False),
                dcc.Graph(id='choroplath')
            ]),
            style={'padding':'20px 50px', 'margin-bottom':20}
        )
    ], style={'padding-left': 50, 'padding-right': 50, 'padding-top': 25, 'padding-bottom': 25, 'background-color': '#E5E5E5'})
])

##################################################################

@app.callback(
    Output('choroplath', 'figure'),
    [Input('dropdown-year', 'value'), Input('checkbox-crime', 'value')]
)
def update_output(year, crimes):
    crimes = ['Municipio'] + crimes
    crimes_pattern = get_crimes_pattern(year, crimes)

    geo_json = get_geo_json()
    fig5 = get_choropleth_fig(crimes_pattern, geo_json)

    return fig5

##################################################################

@app.callback(
    Output('bar-city', 'figure'),
    [Input('dropdown-city', 'value'), Input('checkbox-year', 'value')]
)
def update_crimes_cities(cities, years):
    df_cities = get_year_city(cities, years)
    fig = get_bar_fig_cities(df_cities)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
