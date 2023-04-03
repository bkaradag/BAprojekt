import json
import plotly
import plotly.graph_objs as go
from dateutil.relativedelta import relativedelta
from flask import render_template, request
from datetime import datetime
from database import get_stationen_bodenfeuchte, get_bodenfeuchte_data


def get_bodenfeuchte():
    if request.method == 'POST':
        # HTML formundan seçilen istasyon ID'si alınır
        selected_id = request.form.get('station')
        if not selected_id:
            return "Ein Station auswaehlen."

        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')

        if request.form.get('show_today'):
            today = datetime.date.today()
            start_date_str = today.strftime('%Y-%m-%d')
            end_date_str = today.strftime('%Y-%m-%d')

        elif request.form.get('show_monthh'):
            today = datetime.date.today()
            end_date_str = today.replace(day=1) + relativedelta(months=1) - relativedelta(days=1)
            start_date_str = today.replace(day=1)


        if not (start_date_str and end_date_str):
            return "Zeitraum auswaehlen."
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
        return render_template('bodenfeuchte.html', grafik1JSON=grafik1JSON)
    else:
        # istek methodu GET ise, sayfayı görüntüle
        stations = get_stationen_bodenfeuchte()
        return render_template('bodenfeuchte.html', stations=stations)
        # stations = get_stationen_bodenfeuchte()
        # selected_id = '00082'
        # today = datetime.date.today()
        # start_date_str = today.strftime('%Y-%m-%d')
        # end_date_str = today.strftime('%Y-%m-%d')
        # datum, vgsl = get_bodenfeuchte_data(selected_id, start_date_str, end_date_str)
        #
        # # Plotly grafiklerini oluştur
        # fig1 = go.Figure()
        # fig1.add_trace(go.Line(x=datum, y=vgsl, name='vgsl'))
        #
        # # Grafik ayarlarını yap
        # fig1.update_layout(title='Hava Durumu', xaxis_title='Datum', yaxis_title='VGSL')
        #
        # # Grafikleri HTML olarak döndür
        # grafik1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('bodenfeuchte.html', stations=stations, grafik1JSON=grafik1JSON)