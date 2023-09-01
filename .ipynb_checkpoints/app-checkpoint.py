import dash
from dash import html, dcc, dash_table
from dash import dash_table
from dash.dash_table.Format import Format, Scheme, Symbol
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date
import geopandas as gpd
import json
import os
from graphs import *
#rom funcs import filter_data, kpis
#from graphs_drawer import get_indicator_plot, get_top_province_graph, get_sales_profit_graph, data_bars, get_available_categories, data_bars_diverging

card_height_s = '18rem'
card_height = '34rem'
app = dash.Dash(external_stylesheets=["assets/html-components.css", dbc.themes.BOOTSTRAP])

server = app.server
cwd = os.getcwd()
processed_dir = cwd + "/../Datos/processed/"
graphs_dir = cwd + "/../graphs/"
df = pd.read_csv(processed_dir + "datos_limpios_unidos.csv")
df_map = gpd.read_file(processed_dir + "mc_barrios.shp")
logo_image = "assets/kfc.png"

canales = sorted(df["canal"].unique())
restaurantes = sorted(df["nom_rest"].unique())
total_ventas = df.groupby(['nom_rest', 'canal'])['valor_trans'].sum().reset_index()

###--------- FILTROS-----------------###
date_filter = html.Div([
    dbc.Label("Período", html_for="date-filter"),
    dcc.DatePickerRange(
        id="date-filter",
        start_date=date(2022, 1, 1),
        end_date=date(2022, 12, 30),
        display_format='D MMM YYYY',
        style={
            'display': 'flex',
            'justify-content': 'center',
            'height': '80px',
            'width': '100%'
        }
    )],
)

canal_filter = html.Div([
    dbc.Label("Canal", html_for="category_canal"),
    dcc.Dropdown(
        id="category_canal",
        placeholder='Todos los Canales',
        value=[],
        options=[{'label': canal, 'value': canal} for canal in canales],
        multi=True,
        style={
            'height': '40px'
        }
    )],

)
restaurante_filter = html.Div([
    dbc.Label("Restaurantes", html_for="category_restaurant"),
    dcc.Dropdown(
        id="category_restaurant",
        placeholder='Todos los Restaurantes',
        value=None,
        options=[{'label': rest, 'value': rest} for rest in restaurantes],
        multi=True,
        
        style={
            'height': '40px'
        }
    )],

)
###-----------elementos ------------###
principal_label = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col(
                html.Img(src=logo_image, style={'height': '100px', 'width': 'auto'}),width=4),
            dbc.Col([
                html.Label(
                    "ANÁLISIS DE DATOS ACTUALES.",
                    className="title-enunciado"
                ),
                
            ],width=8),      
            #dbc.Col(canal_filter, align="right", width=4 ),
        ]),
        html.Label(
                    "Se lleva a cabo un análisis exhaustivo utilizando los datos actuales de la empresa, y se facilita su comprensión mediante visualización detallada.",
                    className="texto-enunciado"
                ),  
    ],
    style={
            'height': '10rem',
        }
    )
])
canal_tiempo = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Label(
                    "Venta por canal en el tiempo",
                    className="analisis-title"
                ),
                html.Label(
                    "Total venta por canal en el tiempo, puede cambiar el canal y la fecha ",
                    className="texto-graficos"
                ),
            ],width=8),      
            #dbc.Col(canal_filter, align="right", width=4 ),
        ]),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='line-chart-valor-trans', style={'height': '25rem'})
            )
        )
    ],
    style={
            'height': card_height,
        }
    )
])
transacciones_canal = dbc.Card([
       dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Label(
                    "Transacciones por Canal",
                    className="analisis-title"
                ),
                html.Label(
                    "Porcentajes de transacciones por canal",
                    className="texto-graficos"
                ),
            ],width=8),      
           # dbc.Col(canal_filter, align="right", width=4 ),
        ]),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='pie-chart-percentage-trans-canal', style={'height': '25rem'})
            )
        )
    ],
    style={
            'height': card_height,
        }
    )
])

venta_restaurante_canal = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Label(
                    "Total Venta por restaurante y canal",
                    className="analisis-title"
                ),
                html.Label(
                    "....",
                    className="texto-graficos"
                ),
            ],width=8),      
            #dbc.Col(restaurante_filter, align="right", width=4 ),
        ]),
        dbc.Row([
            
            
           dbc.Col([
                dcc.Graph(id='bar_chart_canal_por_restaurante', style={'height': '28rem'})
            ]),
            
        ]),
    ],
    style={
            'height': card_height,
        }
    )
])

venta_canal = dbc.Card([
    dbc.CardBody([
        dbc.Row([
             dbc.Col(
                dcc.Graph(id='grafico_transacciones_por_canal_y_restaurante', style={'height': '18rem'},className="grafico")
            ),
            
        ]),
    ],
    style={
            'height': card_height_s,
        }
    )
])

ventas_totales_restaurantes = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Label(
                    "Total Venta y comisión por restaurante",
                    className="doble-title"
                )
            ],width=12  )      
            # dbc.Col(restaurante_filter, align="right", width=4),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='bar-chart-valor-trans-restaurante', style={'height': '28rem'})
            ]),
            dbc.Col(
                dcc.Graph(id='bar_chart_comision_por_restaurante', style={'height': '28rem'})
            ),
        ]),
    ],
    style={
        'height': card_height,
    }
)])
filters = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col(
                date_filter,
                width=4
            ),
            dbc.Col(
                canal_filter,
                width=4
            ),
            dbc.Col(
                restaurante_filter,
                width=4
            ),
        ]),
       ],
    style={
        'height': '10rem',
    }
)])


###--------- LAYAUT-----------------###
app.layout = html.Div(children=[
    dbc.Row([
        dbc.Col([
            html.Label(
                "KFC", className="title"
            ), 
        ],width=12),
    ]),    
    dbc.Row([
        dbc.Col(
            principal_label,
            width=8
        ),
        dbc.Col([filters],width=4),
    ]),
    dbc.Row([
        dbc.Col(venta_canal, width=12),
       
    ],style={'margin-top': '8px',
              'margin-bottom': '0px'}),
    dbc.Row([
        dbc.Col(canal_tiempo, width=8),
        dbc.Col(transacciones_canal, width=4),
    ],style={'margin-top': '8px',
              'margin-bottom': '0px'}),
    dbc.Row([
        dbc.Col(venta_restaurante_canal, width=6),
        dbc.Col([
            dash_table.DataTable(
                id='tabla-ventas',
                columns=[
                    {'name': 'Restaurante', 'id': 'nom_rest'},
                    {'name': 'Canal', 'id': 'canal'},
                    {'name': 'Total Ventas', 'id': 'valor_trans', 'type': 'numeric', 'format': Format(symbol='$')},
                ],
                data=total_ventas.to_dict('records'),
                style_table={'width': '100%', 'height': '550px', 'overflowY': 'scroll', 'margin': 'auto'},
                style_header={'backgroundColor': '#a3080c', 'color': 'white'},
                style_cell={'textAlign': 'center'},
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#f9f9f9'},
                    {'if': {'column_id': 'valor_trans'}, 'fontWeight': 'bold'},
                ],
                page_size=16,  # Establece el número de filas visibles en la tabla (puedes ajustar este valor)
            )

            ]),
    ],style={'margin-top': '8px',
              'margin-bottom': '0px'}),
    dbc.Row([
        dbc.Col(ventas_totales_restaurantes, width=12),
        #dbc.Col(dcc.Graph(id='line-chart-valor-trans'), width=6),
    ],style={'margin-top': '8px',
              'margin-bottom': '0px'}),
])  

@app.callback(
    Output('line-chart-valor-trans', 'figure'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date')]
)
def update_line_chart_valor(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df.copy()

    if selected_restaurants:
        filtered_df = filtered_df[filtered_df['nom_rest'].isin(selected_restaurants)]
    
    if selected_canales:
        filtered_df = filtered_df[filtered_df['canal'].isin(selected_canales)]
        
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['fecha_trans'] >= start_date) & (filtered_df['fecha_trans'] <= end_date)]

    fig = generate_line_chart_valor_trans_por_fecha(filtered_df)
    
    # Aquí puedes aplicar las actualizaciones de diseño específicas para este gráfico
    fig.update_layout(
        # Agrega opciones de diseño adicionales aquí
        # Por ejemplo, cambiar el título, el título del eje X, etc.
    )
    
    return fig

@app.callback(
    Output('bar-chart-valor-trans-restaurante', 'figure'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date')]
)
def update_bar_chart_valor(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df.copy()

    if selected_restaurants:
        filtered_df = filtered_df[filtered_df['nom_rest'].isin(selected_restaurants)]
    
    if selected_canales:
        filtered_df = filtered_df[filtered_df['canal'].isin(selected_canales)]
      
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['fecha_trans'] >= start_date) & (filtered_df['fecha_trans'] <= end_date)]

    fig = generate_bar_chart_valor_trans_por_restaurante(filtered_df)
    
    # Aquí puedes aplicar las actualizaciones de diseño específicas para este gráfico
    fig.update_layout(
        # Agrega opciones de diseño adicionales aquí
        # Por ejemplo, cambiar el título, el título del eje X, etc.
    )
    
    return fig

@app.callback(
    Output('pie-chart-percentage-trans-canal', 'figure'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date')]
)
def update_bar_chart_percentage(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df.copy()

    if selected_restaurants:
        filtered_df = filtered_df[filtered_df['nom_rest'].isin(selected_restaurants)]
    
    if selected_canales:
        filtered_df = filtered_df[filtered_df['canal'].isin(selected_canales)]
    
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['fecha_trans'] >= start_date) & (filtered_df['fecha_trans'] <= end_date)]

    fig = generate_pie_chart_percentage_por_canal(filtered_df)
    
    # Aquí puedes aplicar las actualizaciones de diseño específicas para este gráfico
    fig.update_layout(
        # Agrega opciones de diseño adicionales aquí
        # Por ejemplo, cambiar el título, el título del eje X, etc.
    )
    
    return fig
@app.callback(
    Output('bar_chart_comision_por_restaurante', 'figure'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date')]
)
def update_bar_chart_comision(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df.copy()

    if selected_restaurants:
        filtered_df = filtered_df[filtered_df['nom_rest'].isin(selected_restaurants)]
    
    if selected_canales:
        filtered_df = filtered_df[filtered_df['canal'].isin(selected_canales)]
    
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['fecha_trans'] >= start_date) & (filtered_df['fecha_trans'] <= end_date)]

    fig = generate_bar_chart_comision_por_restaurante(filtered_df)
    
    # Aquí puedes aplicar las actualizaciones de diseño específicas para este gráfico
    fig.update_layout(
        # Agrega opciones de diseño adicionales aquí
        # Por ejemplo, cambiar el título, el título del eje X, etc.
    )
    
    return fig

@app.callback(
    Output('bar_chart_canal_por_restaurante', 'figure'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date')]
)
def update_bar_chart_canal(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df.copy()

    if selected_restaurants:
        filtered_df = filtered_df[filtered_df['nom_rest'].isin(selected_restaurants)]
    
    if selected_canales:
        filtered_df = filtered_df[filtered_df['canal'].isin(selected_canales)]
    
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['fecha_trans'] >= start_date) & (filtered_df['fecha_trans'] <= end_date)]

    fig = generate_bar_chart_canal_por_restaurante(filtered_df)
    
    # Aquí puedes aplicar las actualizaciones de diseño específicas para este gráfico
    
    return fig

@app.callback(
    Output('grafico_transacciones_por_canal_y_restaurante', 'figure'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date')]
)
def update_transacciones_por_canal_y_restaurante(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df.copy()

    if selected_restaurants:
        filtered_df = filtered_df[filtered_df['nom_rest'].isin(selected_restaurants)]
    
    if selected_canales:
        filtered_df = filtered_df[filtered_df['canal'].isin(selected_canales)]
    
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['fecha_trans'] >= start_date) & (filtered_df['fecha_trans'] <= end_date)]

    fig = grafico_transacciones_por_canal_y_restaurante(filtered_df)
    
    # Aquí puedes aplicar las actualizaciones de diseño específicas para este gráfico
    
    return fig

@app.callback(
    Output('tabla-ventas', 'data'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date')]
)
def update_table_data(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df.copy()

    if selected_restaurants:
        filtered_df = filtered_df[filtered_df['nom_rest'].isin(selected_restaurants)]
    
    if selected_canales:
        filtered_df = filtered_df[filtered_df['canal'].isin(selected_canales)]
    
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['fecha_trans'] >= start_date) & (filtered_df['fecha_trans'] <= end_date)]

    total_ventas_data = filtered_df.groupby(['nom_rest', 'canal'])['valor_trans'].sum().reset_index()
    
    return total_ventas_data.to_dict('records')

if __name__ == "__main__":
    app.run_server(port=8881, debug=True)








