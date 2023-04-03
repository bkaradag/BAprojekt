import json
import plotly
import plotly.graph_objs as go
from flask import render_template, request

from database import get_stationen_bodenfeuchte
from berechnen import berechnen_campus_wetter_daten


def get_campuswetter():
    if request.method == 'POST':

        datum_ser, temp_ser, rel_feuchte_ser, wind_gesch_ser, luft_druck_ser, luft_druck_ser, \
        global_st_ser, strahlug_bilanz_ser, niederschlag_10m_ser, niederschlag_tag_ser, uv_index_ser, m_mw_list, \
        j_mw_list, zj_mw_list = berechnen_campus_wetter_daten()

        # Plotly grafiklerini oluştur
        fig1 = go.Figure()
        fig1.add_trace(go.Line(x=datum_ser, y=temp_ser, name='Temperatur'))
        # ortalama degerlerini yerlestir
        fig1.add_trace(go.Line(x=m_mw_list[0].index, y=m_mw_list[0].values, name='Mittelwert Monat'))
        fig1.add_trace(go.Line(x=j_mw_list[0].index, y=j_mw_list[0].values, name='Mittelwert Jahr'))
        fig1.add_trace(go.Line(x=j_mw_list[0].index, y=j_mw_list[0].values, name='Mittelwert 10 Jahre'))
        # Grafik ayarlarını yap
        fig1.update_layout(title='Temperatur', xaxis_title='Datum', yaxis_title='Temperatur')
        # Grafikleri HTML olarak döndür
        graf1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

        fig2 = go.Figure()
        fig2.add_trace(go.Line(x=datum_ser, y=rel_feuchte_ser, name='rel_feuchte'))
        fig2.add_trace(go.Line(x=m_mw_list[1].index, y=m_mw_list[1].values, name='Mittelwert Monat'))
        fig2.add_trace(go.Line(x=j_mw_list[1].index, y=j_mw_list[1].values, name='Mittelwert Jahr'))
        fig2.add_trace(go.Line(x=j_mw_list[1].index, y=j_mw_list[1].values, name='Mittelwert 10 Jahre'))
        fig2.update_layout(title='Relative Feuchte', xaxis_title='Datum', yaxis_title='Relative Feuchte')
        graf2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

        fig3 = go.Figure()
        fig3.add_trace(go.Line(x=datum_ser, y=wind_gesch_ser, name='wind_gesch'))
        fig3.add_trace(go.Line(x=m_mw_list[2].index, y=m_mw_list[2].values, name='Mittelwert Monat'))
        fig3.add_trace(go.Line(x=j_mw_list[2].index, y=j_mw_list[2].values, name='Mittelwert Jahr'))
        fig3.add_trace(go.Line(x=j_mw_list[2].index, y=j_mw_list[2].values, name='Mittelwert 10 Jahre'))
        fig3.update_layout(title='Wind Geschwindigkeit', xaxis_title='Datum', yaxis_title='Wind Geschwindigkeit')
        graf3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

        fig4 = go.Figure()
        fig4.add_trace(go.Line(x=datum_ser, y=luft_druck_ser, name='luft_druck'))
        fig4.add_trace(go.Line(x=m_mw_list[3].index, y=m_mw_list[3].values, name='Mittelwert Monat'))
        fig4.add_trace(go.Line(x=j_mw_list[3].index, y=j_mw_list[3].values, name='Mittelwert Jahr'))
        fig4.add_trace(go.Line(x=j_mw_list[3].index, y=j_mw_list[3].values, name='Mittelwert 10 Jahre'))
        fig4.update_layout(title='Luftdruck', xaxis_title='Datum', yaxis_title='Luftdruck')
        graf4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

        fig5 = go.Figure()
        fig5.add_trace(go.Line(x=datum_ser, y=global_st_ser, name='global_str'))
        fig5.add_trace(go.Line(x=m_mw_list[4].index, y=m_mw_list[4].values, name='Mittelwert Monat'))
        fig5.add_trace(go.Line(x=j_mw_list[4].index, y=j_mw_list[4].values, name='Mittelwert Jahr'))
        fig5.add_trace(go.Line(x=j_mw_list[4].index, y=j_mw_list[4].values, name='Mittelwert 10 Jahre'))
        fig5.update_layout(title='Globalstrahlung', xaxis_title='Datum', yaxis_title='Globalstrahlung')
        graf5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)

        fig6 = go.Figure()
        fig6.add_trace(go.Line(x=datum_ser, y=strahlug_bilanz_ser, name='strahlug_bilanz'))
        fig6.add_trace(go.Line(x=m_mw_list[5].index, y=m_mw_list[5].values, name='Mittelwert Monat'))
        fig6.add_trace(go.Line(x=j_mw_list[5].index, y=j_mw_list[5].values, name='Mittelwert Jahr'))
        fig6.add_trace(go.Line(x=j_mw_list[5].index, y=j_mw_list[5].values, name='Mittelwert 10 Jahre'))
        fig6.update_layout(title='Strahlung Bilanz', xaxis_title='Datum', yaxis_title='Strahlung Bilanz')
        graf6JSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)

        fig7 = go.Figure()
        fig7.add_trace(go.Line(x=datum_ser, y=niederschlag_10m_ser, name='niederschlag_10m'))
        fig7.add_trace(go.Line(x=m_mw_list[6].index, y=m_mw_list[6].values, name='Mittelwert Monat'))
        fig7.add_trace(go.Line(x=j_mw_list[6].index, y=j_mw_list[6].values, name='Mittelwert Jahr'))
        fig7.add_trace(go.Line(x=j_mw_list[6].index, y=j_mw_list[6].values, name='Mittelwert 10 Jahre'))
        fig7.update_layout(title='Niederschlag 10Min', xaxis_title='Datum', yaxis_title='Niederschlag 10Min')
        graf7JSON = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)

        fig8 = go.Figure()
        fig8.add_trace(go.Line(x=datum_ser, y=niederschlag_tag_ser, name='niederschlag_tag'))
        fig8.add_trace(go.Line(x=m_mw_list[7].index, y=m_mw_list[7].values, name='Mittelwert Monat'))
        fig8.add_trace(go.Line(x=j_mw_list[7].index, y=j_mw_list[7].values, name='Mittelwert Jahr'))
        fig8.add_trace(go.Line(x=j_mw_list[7].index, y=j_mw_list[7].values, name='Mittelwert 10 Jahre'))
        fig8.update_layout(title='Niederschalg Tag', xaxis_title='Datum', yaxis_title='Niederschalg Tag')
        graf8JSON = json.dumps(fig8, cls=plotly.utils.PlotlyJSONEncoder)

        fig9 = go.Figure()
        fig9.add_trace(go.Line(x=datum_ser, y=uv_index_ser, name='uv_index'))
        fig9.add_trace(go.Line(x=m_mw_list[8].index, y=m_mw_list[8].values,
                               name='Mittelwert Monat'))  # date cikti diye tüm degerler -1 kayiyor (berechnen.py)
        fig9.add_trace(go.Line(x=j_mw_list[8].index, y=j_mw_list[8].values, name='Mittelwert Jahr'))
        fig9.add_trace(go.Line(x=j_mw_list[8].index, y=j_mw_list[8].values, name='Mittelwert 10 Jahre'))
        fig9.update_layout(title='UV-Index', xaxis_title='Datum', yaxis_title='UV-Index')
        graf9JSON = json.dumps(fig9, cls=plotly.utils.PlotlyJSONEncoder)

        # Şablonu render et
        return render_template('campuswetterhoexter.html', graf1JSON=graf1JSON, graf2JSON=graf2JSON,
                               graf3JSON=graf3JSON, graf4JSON=graf4JSON, graf5JSON=graf5JSON, graf6JSON=graf6JSON,
                               graf7JSON=graf7JSON, graf8JSON=graf8JSON, graf9JSON=graf9JSON)
    else:
        # istek methodu GET ise, sayfayı görüntüle
        stations = get_stationen_bodenfeuchte()
        return render_template('campuswetterhoexter.html', stations=stations)