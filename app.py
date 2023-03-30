import json

import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
import plotly
from datetime import datetime
from database import get_stationen_bodenfeuchte, get_bodenfeuchte_data, get_campus_wetter_data, get_map_daten, conn
from berechnen import berechnen_campus_wetter_daten
import folium

app = Flask(__name__)
app.config.suppress_callback_exceptions = True

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/stations')
def get_map():

    # baslangic yeri
    map = folium.Map(location=[48.78, 9.18], zoom_start=10)

    #istasyonlari bir gruba ceviriyor
    fg = folium.FeatureGroup(name="Stations")

    map_daten = get_map_daten()

    for row in map_daten:
        Stationsindex, Breite, Länge = row
        marker = folium.Marker(location=[Breite, Länge], popup=f"Station {Stationsindex}")
        marker.add_to(fg)
    fg.add_to(map)

    map.save('stations.html')
    return render_template('stations.html', stations=map_daten)



@app.route('/dashboard',methods=['GET', 'POST'])
def get_dashboard():
 if request.method == 'POST':
     # HTML formundan seçilen istasyon ID'si alınır
    selected_id = request.form.get('station')
    if not selected_id:
        return "Lütfen bir istasyon seçin."

    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    if not (start_date_str and end_date_str):
        return "Lütfen bir tarih aralığı seçin."
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    datum, vgsl = get_bodenfeuchte_data(selected_id, start_date, end_date)

 # Plotly grafiklerini oluştur
    fig1 = go.Figure()
    fig1.add_trace(go.Line(x=datum, y=vgsl, name='vgsl'))

    # Grafik ayarlarını yap
    fig1.update_layout(title='Hava Durumu', xaxis_title='Datum', yaxis_title='VGSL')

    # Grafikleri HTML olarak döndür
    grafik1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    # Şablonu render et   grafik1JSON=grafik1JSON
    return render_template('dashboard.html', grafik1JSON=grafik1JSON)
 else:
     # istek methodu GET ise, sayfayı görüntüle
        stations = get_stationen_bodenfeuchte()
        return render_template('dashboard.html', stations=stations)



@app.route('/campuswetterhoexter',methods=['GET', 'POST'])
def get_campuswetter():
    if request.method == 'POST':

        datum, temperatur, rel_feuchte, wind_gesch, luft_druck, global_str, strahlug_bilanz, niederschlag_10m, niederschlag_tag, uv_index = get_campus_wetter_data()
        #datum_ser,temp_ser = berechnen_campus_wetter_daten()

        # fig1 = go.Figure()
        # fig1.add_trace(go.Line(x=datum_ser, y=temp_ser, name='Temperatur'))
        # fig1.add_trace(go.Line(x=m_mw_list[1].index, y=m_mw_list[1].values, name='Aylık Ortalama'))
        # fig1.add_trace(go.Line(x=j_mw_list[1].index, y=j_mw_list[1].values, name='Yıllık Ortalama'))
        # fig1.add_trace(go.Line(x=j_mw_list[1].index, y=j_mw_list[1].values, name='10 Yıllık Ortalama'))
        # fig1.update_layout(title='Temperatur', xaxis_title='Datum', yaxis_title='Temperatur')
        # graf1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)


        # # Plotly grafiklerini oluştur
        # fig1 = go.Figure()
        # fig1.add_trace(go.Line(x=datum_series, y=temperatur_series, name='Temperatur'))
        # # Aylık Ortalama Çizgisi Ekleme
        #
        # fig1.add_trace(go.Line(x=monthly_avg.index, y=monthly_avg.values, name='Aylık Ortalama'))
        #
        # # Yıllık Ortalama Çizgisi Ekleme
        # yearly_avg = temperatur_series.resample('Y').mean()
        # fig1.add_trace(go.Line(x=yearly_avg.index, y=yearly_avg.values, name='Yıllık Ortalama'))
        #
        # # 10 Yıllık Ortalama Çizgisi Ekleme
        # ten_year_avg = temperatur_series.resample('10Y').mean()
        # fig1.add_trace(go.Line(x=ten_year_avg.index, y=ten_year_avg.values, name='10 Yıllık Ortalama'))
        #
        # fig1.update_layout(title='Temperatur', xaxis_title='Datum', yaxis_title='Temperatur')
        # graf1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

        # fig1.add_trace(
        #     go.Line(x=[min(datum), max(datum)], y=[m_mw_temperatur, m_mw_temperatur], name='Mittelwert Monat'))
        # fig1.add_trace(
        #     go.Line(x=[min(datum), max(datum)], y=[j_mw_temperatur, j_mw_temperatur], name='Mittelwert 1 Jahr'))
        # fig1.add_trace(
        #     go.Line(x=[min(datum), max(datum)], y=[zj_mw_temperatur, zj_mw_temperatur], name='Mittelwert 10 Jahre'))

        # fig2 = go.Figure()
        # fig2.add_trace(go.Line(x=datum, y=rel_feuchte, name='rel_feuchte'))
        # # fig1.add_trace(go.Line(x=[min(datum), max(datum)], y=m_mw_rel_feuchte, name='Mittelwert Monat'))
        # # fig1.add_trace(go.Line(x=[min(datum), max(datum)], y=[j_mw_temperatur, j_mw_temperatur], name='Mittelwert 1 Jahr'))
        # # fig1.add_trace(go.Line(x=[min(datum), max(datum)], y=[zj_mittelwert, zj_mittelwert], name='Mittelwert 10 Jahre'))
        #
        fig3 = go.Figure()
        fig3.add_trace(go.Line(x=datum, y=wind_gesch, name='wind_gesch'))
        #
        # fig4 = go.Figure()
        # fig4.add_trace(go.Line(x=datum, y=luft_druck, name='luft_druck'))
        #
        # fig5 = go.Figure()
        # fig5.add_trace(go.Line(x=datum, y=global_str, name='global_str'))
        #
        # fig6 = go.Figure()
        # fig6.add_trace(go.Line(x=datum, y=strahlug_bilanz, name='strahlug_bilanz'))
        #
        # fig7 = go.Figure()
        # fig7.add_trace(go.Line(x=datum, y=niederschlag_10m, name='niederschlag_10m'))
        #
        # fig8 = go.Figure()
        # fig8.add_trace(go.Line(x=datum, y=niederschlag_tag, name='niederschlag_tag'))
        #
        # fig9 = go.Figure()
        # fig9.add_trace(go.Line(x=datum, y=uv_index, name='uv_index'))

    # Grafik ayarlarını yap

        # fig2.update_layout(title='Relative Feuchte', xaxis_title='Datum', yaxis_title='Relative Feuchte')
        fig3.update_layout(title='Wind Geschwindigkeit', xaxis_title='Datum', yaxis_title='Wind Geschwindigkeit')
        # fig4.update_layout(title='Luftdruck', xaxis_title='Datum', yaxis_title='Luftdruck')
        # fig5.update_layout(title='Globalstrahlung', xaxis_title='Datum', yaxis_title='Globalstrahlung')
        # fig6.update_layout(title='Strahlung Bilanz', xaxis_title='Datum', yaxis_title='Strahlung Bilanz')
        # fig7.update_layout(title='Niederschlag 10Min', xaxis_title='Datum', yaxis_title='Niederschlag 10Min')
        # fig8.update_layout(title='Niederschalg Tag', xaxis_title='Datum', yaxis_title='Niederschalg Tag')
        # fig9.update_layout(title='UV-Index', xaxis_title='Datum', yaxis_title='UV-Index')

    # Grafikleri HTML olarak döndür

        # graf2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        graf3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        # graf4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
        # graf5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
        # graf6JSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)
        # graf7JSON = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)
        # graf8JSON = json.dumps(fig8, cls=plotly.utils.PlotlyJSONEncoder)
        # graf9JSON = json.dumps(fig9, cls=plotly.utils.PlotlyJSONEncoder)

    # Şablonu render et
        return render_template('campuswetterhoexter.html',graf3JSON=graf3JSON)
    else:
        # istek methodu GET ise, sayfayı görüntüle
        stations = get_stationen_bodenfeuchte()
        return render_template('campuswetterhoexter.html', stations=stations)

if __name__ == '__main__':
    app.run(debug=True)
