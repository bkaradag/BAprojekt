import json
import plotly
import plotly.graph_objs as go
from flask import render_template, request

from database import get_brightsky_wind_data
from berechnen import berechnen_brightsky_wind_daten


def get_brightsky_wind():
    if request.method == 'POST':

        datum_ser, wind_richtung_ser, wind_geschw_ser, wind_boe_rich_ser, wind_boe_geschw_ser, m_mw_list, j_mw_list, zj_mw_list = berechnen_brightsky_wind_daten()
        wind_richtung = get_brightsky_wind_data()

        fig1 = go.Figure()
        fig1.add_trace(go.Line(x=datum_ser, y=wind_geschw_ser, name='WindGeschwindigkeit'))
        fig1.add_trace(go.Line(x=m_mw_list[1].index, y=m_mw_list[1].values, name='Mittelwert Monat'))
        fig1.add_trace(go.Line(x=j_mw_list[1].index, y=j_mw_list[1].values, name='Mittelwert Jahr'))
        fig1.add_trace(go.Line(x=j_mw_list[1].index, y=j_mw_list[1].values, name='Mittelwert 10 Jahre'))
        fig1.update_layout(title='Wind Geschwindigkeit', xaxis_title='Datum', yaxis_title='Wind Geschwindigkeit')
        graf1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

        fig2 = go.Figure()
        fig2.add_trace(go.Line(x=datum_ser, y=wind_boe_geschw_ser, name='WindBöeGeschwindigkeit'))
        fig2.add_trace(go.Line(x=m_mw_list[3].index, y=m_mw_list[3].values, name='Mittelwert Monat'))
        fig2.add_trace(go.Line(x=j_mw_list[3].index, y=j_mw_list[3].values, name='Mittelwert Jahr'))
        fig2.add_trace(go.Line(x=j_mw_list[3].index, y=j_mw_list[3].values, name='Mittelwert 10 Jahre'))
        fig2.update_layout(title='Windböegeschwindigkeit', xaxis_title='Datum', yaxis_title='Windböegeschwindigkeit')
        graf2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

        fig3 = go.Figure(go.Barpolar(
            r=[1] * len(wind_richtung),
            theta=wind_richtung,
            marker_color=wind_richtung,
            marker=dict(
                color=wind_richtung,
                colorscale='Viridis',
                showscale=True,
                reversescale=True
            ),
            opacity=0.8
        ))

        fig3.update_layout(
            title='Rüzgar Yönü',
            font_size=16,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                ),
                angularaxis=dict(
                    direction="clockwise",
                    tickmode="array",
                    tickvals=[0, 45, 90, 135, 180, 225, 270, 315],
                    ticktext=["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                    tickfont=dict(size=12),
                    rotation=90
                )
            )
        )
        graf3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

        fig4 = go.Figure(go.Barpolar(
            r=[1] * len(wind_boe_rich_ser),
            theta=wind_boe_rich_ser,
            marker_color=wind_boe_rich_ser,
            marker=dict(
                color=wind_boe_rich_ser,
                colorscale='Viridis',
                showscale=True,
                reversescale=True
            ),
            opacity=0.8
        ))

        fig4.update_layout(
            title='Rüzgar Yönü',
            font_size=16,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                ),
                angularaxis=dict(
                    direction="clockwise",
                    tickmode="array",
                    tickvals=[0, 45, 90, 135, 180, 225, 270, 315],
                    ticktext=["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                    tickfont=dict(size=12),
                    rotation=90
                )
            )
        )
        graf4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)


        # Şablonu render et
        return render_template('brightskywind.html', graf1JSON=graf1JSON, graf2JSON=graf2JSON,
                               graf3JSON=graf3JSON, graf4JSON=graf4JSON)
    else:
        # istek methodu GET ise, sayfayı görüntüle

        return render_template('brightskywind.html')
