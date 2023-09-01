import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
from dash.dash_table.Format import Format, Scheme, Symbol
import pandas as pd
from datetime import date
import geopandas as gpd
import json
import os
from graphs import *

###------------MARGEN
card_height_s = '18rem'
card_height = '34rem'
app = dash.Dash(external_stylesheets=["assets/html-components.css", dbc.themes.BOOTSTRAP])

###------------DATOS
server = app.server
cwd = os.getcwd()
Final_dir = cwd + "/../Datos/Final/"
graphs_dir = cwd + "/../graphs/"
df = pd.read_csv(Final_dir + "final_Datos_presente.csv")
df_futuro = pd.read_csv(Final_dir + "final_Datos_futuro.csv")
logo_image = "assets/kfc.png"

canales = sorted(df["canal"].unique())
restaurantes = sorted(df["nom_rest"].unique())
total_ventas = df.groupby(['nom_rest', 'canal'])['valor_trans'].sum().reset_index()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
date_filter_fut = html.Div([
    dbc.Label("Período", html_for="date-filter"),
    dcc.DatePickerRange(
        id="date-filter-fut",
        start_date=date(2023, 5, 1),
        end_date=date(2023, 8, 30),
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
principal_label_Act = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col(
                html.Img(src=logo_image, style={'height': '100px', 'width': '50%'}),width=4),
            dbc.Col([
                html.Label(
                    "ANÁLISIS DE DATOS ACTUALES.",
                    className="title-enunciado"
                ),
                
            ],width=8),      
            #dbc.Col(canal_filter, align="right", width=4 ),
        ]), 
    ],
    style={
            'height': '10rem',
        }
    )
])
principal_label_Fut = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col(
                html.Img(src=logo_image, style={'height': '100px', 'width': '50%'}),width=4),
            dbc.Col([
                html.Label(
                    "ANÁLISIS DE DATOS PREDICCIÓN.",
                    className="title-enunciado"
                ),
                
            ],width=8),      
            #dbc.Col(canal_filter, align="right", width=4 ),
        ]), 
    ],
    style={
            'height': '10rem',
        }
    )
])

principal_label_Res = dbc.Card([
    dbc.CardBody([
        dbc.Row([
             dbc.Col(
                html.Img(src=logo_image, style={'height': '100px', 'width': '50%'}),width=3),
            dbc.Col([
                html.Label(
                    "RESUMEN.",
                    className="title-enunciado1"
                ),
                
            ],width=9),      
            #dbc.Col(canal_filter, align="right", width=4 ),
        ]), 
    ],
    style={
            'height': '10rem',
        }
    )
])
resumen_texto = dbc.Card([
    dbc.CardBody([
        dbc.Row([
             dbc.Col([
            html.P("El dashboard está diseñado para aplicar la ciencia de datos y desarrollar un producto de datos que permita predecir la cantidad de transacciones por domicilios de la empresa KFC en la ciudad de Cali. El objetivo principal es mejorar la toma de decisiones dentro de la cadena de suministro y operaciones de la empresa."),
    html.P("El dashboard se compone de las siguientes secciones clave:"),
    html.Ol([
        html.Li("Visualización de datos históricos: Proporciona una visión general de las transacciones de domicilios KFC en Cali a lo largo del tiempo. Se utilizan gráficos interactivos para mostrar tendencias, estacionalidad y patrones históricos relevantes."),
        html.Li("Modelos de predicción: Se implementan modelos de aprendizaje automático para predecir la cantidad de transacciones futuras. Estos modelos están entrenados con datos históricos y se actualizan periódicamente para mejorar la precisión de las predicciones."),
        html.Li("Panel de control ejecutivo: Ofrece un resumen conciso de los resultados más importantes, proporcionando información clave a los tomadores de decisiones de manera rápida y efectiva."),
    ]),
    html.P("El dashboard se presenta en un formato intuitivo y fácil de usar, lo que permite a los diferentes miembros del equipo de KFC en Cali acceder a información relevante y tomar decisiones informadas en tiempo real. La implementación de este producto de datos ayudará a optimizar la cadena de suministro y las operaciones, permitiendo una gestión más eficiente de recursos y mejorando la satisfacción del cliente."),
            
            
            ],className="texto-resumen",width=12),      
        ]), 
    ],
    style={
            'height': '28rem',
        }
    )
])
canal_tiempo_act = dbc.Card([
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

### futuros elementos

filters_fut = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col(
                date_filter_fut,
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
canal_tiempo_fut = dbc.Card([
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
                dcc.Graph(id='line-chart-valor-trans_fut', style={'height': '25rem'})
            )
        )
    ],
    style={
            'height': card_height,
        }
    )
])
transacciones_canal_fut = dbc.Card([
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
                dcc.Graph(id='pie-chart-percentage-trans-canal_fut', style={'height': '25rem'})
            )
        )
    ],
    style={
            'height': card_height,
        }
    )
])

venta_restaurante_canal_fut = dbc.Card([
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
                dcc.Graph(id='bar_chart_canal_por_restaurante_fut', style={'height': '28rem'})
            ]),
            
        ]),
    ],
    style={
            'height': card_height,
        }
    )
])

venta_canal_fut = dbc.Card([
    dbc.CardBody([
        dbc.Row([
             dbc.Col(
                dcc.Graph(id='grafico_transacciones_por_canal_y_restaurante_fut', style={'height': '18rem'},className="grafico")
            ),
            
        ]),
    ],
    style={
            'height': card_height_s,
        }
    )
])

ventas_totales_restaurantes_fut = dbc.Card([
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
                dcc.Graph(id='bar-chart-valor-trans-restaurante_fut', style={'height': '28rem'})
            ]),
            dbc.Col(
                dcc.Graph(id='bar_chart_comision_por_restaurante_fut', style={'height': '28rem'})
            ),
        ]),
    ],
    style={
        'height': card_height,
    }
)])

###---------------DATOS ACTUALES.
# Definimos el contenido de la página de datos actuales
datos_actuales_content = html.Div([
    dbc.Row([
        dbc.Col(
            principal_label_Act,
            width=8
        ),
        dbc.Col([filters],width=4),
    ],style={'margin-top': '16px',
              'margin-bottom': '8px'}),
    dbc.Row([
        dbc.Col(venta_canal, width=12),
       
    ],style={'margin-top': '8px',
              'margin-bottom': '0px'}),
    dbc.Row([
        dbc.Col(canal_tiempo_act, width=8),
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
              'margin-bottom': '0px'})
])
# Definimos el contenido de la página de predicción
prediccion_content = html.Div([
      dbc.Row([
        dbc.Col(
            principal_label_Fut,
            width=8
        ),
        dbc.Col([filters_fut],width=4),
    ],style={'margin-top': '16px',
              'margin-bottom': '8px'}),
    dbc.Row([
        dbc.Col(venta_canal_fut, width=12),
       
    ],style={'margin-top': '8px',
              'margin-bottom': '0px'}),
    dbc.Row([
        dbc.Col(canal_tiempo_fut, width=8),
        dbc.Col(transacciones_canal_fut, width=4),
    ],style={'margin-top': '8px',
              'margin-bottom': '0px'}),
    dbc.Row([
        dbc.Col(venta_restaurante_canal_fut, width=6),
        dbc.Col([
            dash_table.DataTable(
                id='tabla-ventas_fut',
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
        dbc.Col(ventas_totales_restaurantes_fut, width=12),
        #dbc.Col(dcc.Graph(id='line-chart-valor-trans'), width=6),
    ],style={'margin-top': '8px',
              'margin-bottom': '0px'})
])
resumen_content = html.Div([
    dbc.Row([
        dbc.Col(
            principal_label_Res,
            width=12
        )
    ],style={'margin-top': '8px','margin-left': '8px',
              'margin-bottom': '8px'}),
    dbc.Row([
        dbc.Col(resumen_texto, width=12),
       
    ],style={'margin-top': '8px','margin-left': '8px',
              'margin-bottom': '8px'}),
        
])



# Definimos el layout de la página principal
app.layout = html.Div([
       dbc.Row([
        dbc.Col([
            html.Label(
                "KFC", className="title"
            ), 
        ],width=12),
    ]), 
    dcc.Location(id='url', refresh=True),
    dbc.NavbarSimple(
        children=[
            
            dbc.NavItem(dbc.NavLink("Datos Actuales", href="/datos_actuales")),
            dbc.NavItem(dbc.NavLink("Predicción", href="/prediccion"))
        ],
        brand="Página Principal",
        brand_href="/",
        color="#A3080C",
        dark=True,
         
    ),
    # Agregamos un espacio para mostrar el resumen
    html.Div(id="page-content", children=resumen_content)
])

# Definimos las devoluciones de llamada para cambiar el contenido según el botón seleccionado
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/datos_actuales":
        return datos_actuales_content
    elif pathname == "/prediccion":
        return prediccion_content
    else:
        return resumen_content

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


###################################

@app.callback(
    Output('line-chart-valor-trans_fut', 'figure'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter-fut', 'start_date'),
     Input('date-filter-fut', 'end_date')]
)
def update_line_chart_valor_fut(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df_futuro.copy()

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
    Output('bar-chart-valor-trans-restaurante_fut', 'figure'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter-fut', 'start_date'),
     Input('date-filter-fut', 'end_date')]
)
def update_bar_chart_valor_fut(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df_futuro.copy()

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
    Output('pie-chart-percentage-trans-canal_fut', 'figure'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter-fut', 'start_date'),
     Input('date-filter-fut', 'end_date')]
)
def update_bar_chart_percentage_fut(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df_futuro.copy()

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
    Output('bar_chart_comision_por_restaurante_fut', 'figure'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter-fut', 'start_date'),
     Input('date-filter-fut', 'end_date')]
)
def update_bar_chart_comision_fut(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df_futuro.copy()

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
    Output('bar_chart_canal_por_restaurante_fut', 'figure'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter-fut', 'start_date'),
     Input('date-filter-fut', 'end_date')]
)
def update_bar_chart_canal_fut(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df_futuro.copy()

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
    Output('tabla-ventas_fut', 'data'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter-fut', 'start_date'),
     Input('date-filter-fut', 'end_date')]
)
def update_table_data_fut(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df_futuro.copy()

    if selected_restaurants:
        filtered_df = filtered_df[filtered_df['nom_rest'].isin(selected_restaurants)]
    
    if selected_canales:
        filtered_df = filtered_df[filtered_df['canal'].isin(selected_canales)]
    
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['fecha_trans'] >= start_date) & (filtered_df['fecha_trans'] <= end_date)]

    total_ventas_data = filtered_df.groupby(['nom_rest', 'canal'])['valor_trans'].sum().reset_index()
    
    return total_ventas_data.to_dict('records')



@app.callback(
    Output('grafico_transacciones_por_canal_y_restaurante_fut', 'figure'),
    [Input('category_restaurant', 'value'),
     Input('category_canal', 'value'),
     Input('date-filter-fut', 'start_date'),
     Input('date-filter-fut', 'end_date')]
)
def update_transacciones_por_canal_y_restaurante_fut(selected_restaurants, selected_canales, start_date, end_date):
    filtered_df = df_futuro.copy()

    if selected_restaurants:
        filtered_df = filtered_df[filtered_df['nom_rest'].isin(selected_restaurants)]
    
    if selected_canales:
        filtered_df = filtered_df[filtered_df['canal'].isin(selected_canales)]
    
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['fecha_trans'] >= start_date) & (filtered_df['fecha_trans'] <= end_date)]

    fig = grafico_transacciones_por_canal_y_restaurante_f(filtered_df)
    
    # Aquí puedes aplicar las actualizaciones de diseño específicas para este gráfico
    
    return fig


if __name__ == "__main__":
    app.run_server(port=8881, debug=True)
