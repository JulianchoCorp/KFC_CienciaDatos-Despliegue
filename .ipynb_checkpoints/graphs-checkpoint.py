import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#1
def generate_line_chart_valor_trans_por_fecha(df):
    grouped_df = df.groupby(['fecha_trans', 'canal'])['valor_trans'].sum().reset_index()

    fig = go.Figure()

    for canal, data in grouped_df.groupby('canal'):
        fig.add_trace(go.Scatter(
            x=data['fecha_trans'],
            y=data['valor_trans'],
            mode='lines+markers',  # Líneas con marcadores para puntos de datos
            name=canal,
        ))

    fig.update_layout(
        #title_text='Venta por Canal en el Tiempo',
        #xaxis_title='Fecha',
        yaxis_title='Venta',
        showlegend=True
    )

    return fig
#2
def generate_pie_chart_percentage_por_canal(df):
    data = df['canal'].value_counts(normalize=True)
    labels = data.index.tolist()
    values = data.values.tolist()

    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.4,  # Controla el tamaño del agujero en el gráfico de anillo (valor entre 0 y 1)
            textinfo='percent+label',
            insidetextorientation='radial'
        )
    )

    return fig
#3
# Función para generar el gráfico de barras horizontales (comision por restaurante)
def generate_bar_chart_canal_por_restaurante(df):

   # data = df.groupby('nom_rest')['comision'].sum().reset_index()
    #fig = px.bar(data, x='comision', y='nom_rest', orientation='h', title='Comisión por Restaurante')
    #return fig
    grouped_df = df.groupby(['nom_rest', 'canal'])['valor_trans'].sum().reset_index()

    fig = go.Figure()

    for canal, data in grouped_df.groupby('canal'):
        fig.add_trace(go.Bar(
            y=data['nom_rest'],
            x=data['valor_trans'],
            name=canal,
            orientation='h',  # Orientación horizontal
            text=data['valor_trans'].apply(lambda x: f'Canal: {canal}<br>Total Venta: {x}'),
            hoverinfo='text+x',  # Mostrar información personalizada en el hover
        
        ))
    fig.update_layout(
        #title_text='Valor Total de Ventas por Restaurante, subdividido por Canal',
        xaxis_title='Total de Ventas',
        #yaxis_title='Restaurante',
        barmode='stack',  # Barras apiladas para subdividir por canal
        showlegend=True,
        bargap=0.2

    )
    return fig

#5
# Función para generar el gráfico de barras horizontales (valor total de transacción por restaurante)
def generate_bar_chart_valor_trans_por_restaurante(df):
    data = df.groupby('nom_rest')['valor_trans'].sum().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=data['nom_rest'],
        x=data['valor_trans'],
        orientation='h',
        marker_color='#A3080C',  # Establecer el color de las barras a un tono de rojo
    ))

    fig.update_layout(
        #title_text='Venta por Canal en el Tiempo',
        yaxis_title='',
        xaxis_title='Venta',
        showlegend=False,
    )

    return fig
#6
# Función para generar el gráfico lineal (valor total de transacción por fecha)
def generate_bar_chart_comision_por_restaurante(df):
    data = df.groupby('nom_rest')['comision'].sum().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=data['nom_rest'],
        x=data['comision'],
        orientation='h',
        marker_color='#A3080C',  # Establecer el color de las barras a un tono de rojo más oscuro
    ))

    fig.update_layout(
        #title_text='Venta por Canal en el Tiempo',
        yaxis_title='',
        xaxis_title='Comisión',
        showlegend=False,
    )

    return fig


# Función para generar el gráfico de anillo (número o % de transacciones por canal)
def generate_pie_chart_num_por_canal(df):

    data = df['canal'].value_counts().reset_index()
    data.columns = ['canal', 'num_trans']
    fig = px.pie(data, values='num_trans', names='canal', title='Número de Transacciones por Canal')
    return fig

def grafico_transacciones_por_canal_y_restaurante(df):
# Agrupar por canal y contar el número de transacciones para cada canal
    transacciones_por_canal = df.groupby('canal')['cod_trans'].count()

    # Agrupar por restaurante y contar el número de transacciones para cada restaurante
    transacciones_por_restaurante = df.groupby(['canal', 'nom_rest'])['cod_trans'].count().reset_index()

    # Crear la figura de subgráficos
    fig = make_subplots(rows=1, cols=len(transacciones_por_canal), subplot_titles=transacciones_por_canal.index.tolist())

    for i, canal in enumerate(transacciones_por_canal.index.tolist(), 1):
        data = transacciones_por_restaurante[transacciones_por_restaurante['canal'] == canal]
        fig.add_trace(go.Bar(x=data['nom_rest'], y=data['cod_trans'], marker=dict(color='#a3080c')), row=1, col=i)
        fig.update_xaxes( row=1, col=i)
        fig.update_yaxes(title_text='', row=1, col=i)
        
        fig.update_layout(
            height=300,
            width=1800,
            showlegend=False,
            title_text='Transacciones por Canal y Restaurante',
            title_font=dict(size=24, color='#a3080c', family='Arial'),  # Cambiar la fuente del título a Arial
            title_x=0.5
        )
    return fig

def grafico_transacciones_por_canal_y_restaurante_f(df):
    # Calcula el número de transacciones por canal y por restaurante
    transacciones_por_canal = df.groupby('canal')['cod_rest'].count()
    transacciones_por_restaurante = df.groupby(['canal', 'nom_rest'])['cod_rest'].count().reset_index()

    # Crea la figura de subgráficos
    fig = make_subplots(rows=1, cols=len(transacciones_por_canal), subplot_titles=transacciones_por_canal.index.tolist())

    # Itera a través de los canales y agrega barras a la figura
    for i, canal in enumerate(transacciones_por_canal.index.tolist(), 1):
        data = transacciones_por_restaurante[transacciones_por_restaurante['canal'] == canal]
        fig.add_trace(go.Bar(x=data['nom_rest'], y=data['cod_rest'], marker=dict(color='#a3080c')), row=1, col=i)
        fig.update_xaxes(row=1, col=i)
        fig.update_yaxes(title_text='', row=1, col=i)

    # Actualiza el diseño de la figura
    fig.update_layout(
        height=300,
        width=1800,
        showlegend=False,
        title_text='Transacciones por Canal y Restaurante',
        title_font=dict(size=24, color='#a3080c', family='Arial'),
        title_x=0.5
    )
    
    return fig  # Devuelve la figura
