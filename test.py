import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from berechnen import berechnen_campus_wetter_daten

datum_ser, temp_ser, rel_feuchte_ser, wind_gesch_ser, luft_druck_ser, luft_druck_ser, global_st_ser, strahlug_bilanz_ser, niederschlag_10m_ser, niederschlag_tag_ser, uv_index_ser, m_mw_list, j_mw_list, zj_mw_list = berechnen_campus_wetter_daten()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Relative Feuchte"),
    dcc.Graph(id='graph'),
    html.Button('Tablo göster', id='button', n_clicks=0),
    html.Div(id='table-container')
])

@app.callback(
    Output(component_id='table-container', component_property='children'),
    [Input(component_id='button', component_property='n_clicks')]
)
def update_table(n_clicks):
    if n_clicks > 0:
        table = html.Table([
            html.Thead(
                html.Tr([
                    html.Th("Tarih"),
                    html.Th("Nem Orani"),
                ])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(datum),
                    #html.Td("{:.2f}".format(rel_feuchte)),
                    html.Td(rel_feuchte)


                ])
                #for datum,rel_feuchte, m_mw, j_mw, j_10_mw in zip(datum_ser,rel_feuchte_ser, m_mw_list.values, j_mw_list[1].values, j_mw_list[1].values)
                for datum, rel_feuchte in
                zip(datum_ser, rel_feuchte_ser)
            ])
        ])
        return table

@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='button', component_property='n_clicks')]
)
def update_graph(n_clicks):
    fig = go.Figure()
    fig.add_trace(go.Line(x=datum_ser, y=rel_feuchte_ser, name='rel_feuchte'))
    fig.add_trace(go.Line(x=m_mw_list[1].index, y=m_mw_list[1].values, name='Mittelwert Monat'))
    fig.add_trace(go.Line(x=j_mw_list[1].index, y=j_mw_list[1].values, name='Mittelwert Jahr'))
    fig.add_trace(go.Line(x=j_mw_list[1].index, y=j_mw_list[1].values, name='Mittelwert 10 Jahre'))
    fig.update_layout(title='Relative Feuchte', xaxis_title='Datum', yaxis_title='Relative Feuchte')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)