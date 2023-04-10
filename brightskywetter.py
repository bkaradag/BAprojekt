import json
import plotly
import plotly.graph_objs as go
from flask import render_template, request


from berechnen import berechnen_brightsky_wetter_daten


def get_brightsky_wetter():
    if request.method == 'POST':

        datum_ser, niederschlag_ser, luftdruck_ser, relat_feuchte_ser, sonnenschein_ser, temp_ser, m_mw_list, j_mw_list, zj_mw_list = berechnen_brightsky_wetter_daten()

        fig1 = go.Figure()
        fig1.add_trace(go.Line(x=datum_ser, y=temp_ser, name='Temperatur'))
        fig1.add_trace(go.Line(x=m_mw_list[4].index, y=m_mw_list[4].values, name='Mittelwert Monat'))
        fig1.add_trace(go.Line(x=j_mw_list[4].index, y=j_mw_list[4].values, name='Mittelwert Jahr'))
        fig1.add_trace(go.Line(x=j_mw_list[4].index, y=j_mw_list[4].values, name='Mittelwert 10 Jahre'))
        fig1.update_layout(title='Temperatur', xaxis_title='Datum', yaxis_title='Temperatur')
        graf1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

        fig2 = go.Figure()
        fig2.add_trace(go.Line(x=datum_ser, y=relat_feuchte_ser, name='rel_feuchte'))
        fig2.add_trace(go.Line(x=m_mw_list[2].index, y=m_mw_list[2].values, name='Mittelwert Monat'))
        fig2.add_trace(go.Line(x=j_mw_list[2].index, y=j_mw_list[2].values, name='Mittelwert Jahr'))
        fig2.add_trace(go.Line(x=j_mw_list[2].index, y=j_mw_list[2].values, name='Mittelwert 10 Jahre'))
        fig2.update_layout(title='Relative Feuchte', xaxis_title='Datum', yaxis_title='Relative Feuchte')
        graf2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

        fig3 = go.Figure()
        fig3.add_trace(go.Line(x=datum_ser, y=sonnenschein_ser, name='sonnenschein'))
        fig3.add_trace(go.Line(x=m_mw_list[3].index, y=m_mw_list[3].values, name='Mittelwert Monat'))
        fig3.add_trace(go.Line(x=j_mw_list[3].index, y=j_mw_list[3].values, name='Mittelwert Jahr'))
        fig3.add_trace(go.Line(x=j_mw_list[3].index, y=j_mw_list[3].values, name='Mittelwert 10 Jahre'))
        fig3.update_layout(title='Sonnenschein', xaxis_title='Datum', yaxis_title='Sonnenschein')
        graf3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

        fig4 = go.Figure()
        fig4.add_trace(go.Line(x=datum_ser, y=luftdruck_ser, name='luft_druck'))
        fig4.add_trace(go.Line(x=m_mw_list[1].index, y=m_mw_list[1].values, name='Mittelwert Monat'))
        fig4.add_trace(go.Line(x=j_mw_list[1].index, y=j_mw_list[1].values, name='Mittelwert Jahr'))
        fig4.add_trace(go.Line(x=j_mw_list[1].index, y=j_mw_list[1].values, name='Mittelwert 10 Jahre'))
        fig4.update_layout(title='Luftdruck', xaxis_title='Datum', yaxis_title='Luftdruck')
        graf4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

        fig5 = go.Figure()
        fig5.add_trace(go.Line(x=datum_ser, y=niederschlag_ser, name='niederschlag'))
        fig5.add_trace(go.Line(x=m_mw_list[0].index, y=m_mw_list[0].values, name='Mittelwert Monat'))
        fig5.add_trace(go.Line(x=j_mw_list[0].index, y=j_mw_list[0].values, name='Mittelwert Jahr'))
        fig5.add_trace(go.Line(x=j_mw_list[0].index, y=j_mw_list[0].values, name='Mittelwert 10 Jahre'))
        fig5.update_layout(title='Niederschlag', xaxis_title='Datum', yaxis_title='Niederschlag')
        graf5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)

        # Şablonu render et
        return render_template('brightskywetter.html', graf1JSON=graf1JSON, graf2JSON=graf2JSON,
                               graf3JSON=graf3JSON, graf4JSON=graf4JSON, graf5JSON=graf5JSON)
    else:
        # istek methodu GET ise, sayfayı görüntüle

        return render_template('brightskywetter.html')