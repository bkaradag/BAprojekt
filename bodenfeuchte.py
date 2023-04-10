import json
import plotly
import plotly.graph_objs as go
from dateutil.relativedelta import relativedelta
from flask import request
from datetime import datetime
from database import get_bodenfeuchte_data


def get_bodenfeuchte():
    if request.method == 'POST': # TODO: yorum satirlari ekle
        selected_id = request.form.get('station')
        print(selected_id + "selected_id")
        if not selected_id:
            return "Ein Station auswaehlen."

        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        print(start_date_str + "start_date_str")
        print(end_date_str + "end_date_str")

        if request.form.get('show_today'): #TODO: gün ve ay butonlarini aktif et
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

        datum, vgsl, vpgb, vpgpm, vpgh, vpmb, vpzb, vgls, vwls, vwsl, ts05, ts10, ts20, \
        ts50, ts100, tsls05, bf10, bf20, bf30, bf40, bf50, bf60, bfgls, bfgsl, bfwls, bfwsl, \
        zfumi, ztkmi, ztumi = get_bodenfeuchte_data(selected_id, start_date, end_date)

        # Hauptgrafik TODO: dwd grafigi buraya gelecek, tagesniederschlag eklenmesi gerekiyor
        fig1 = go.Figure()

        fig1.add_trace(go.Line(x=datum, y=bfgls, name='Bodenfeuchte unter Gras bei lehmigen Sand zwischen 0-60cm'))
        fig1.add_trace(go.Line(x=datum, y=bfgsl, name='Bodenfeuchte unter Gras bei sandigem Lehm zwischen 0-60cm'))
        fig1.add_trace(go.Bar(x=datum, y=bf30, name='Bodenfeuchte unter Gras bei sandigem Lehm zwischen 20-30cm'))

        fig1.update_layout(title='Bodenfeuchte', xaxis_title='Datum', yaxis_title='Bodenfeuchte (%nFK)',
                           legend=dict(orientation='h', yanchor='bottom', y=-1.02, xanchor='center', x=0.5))
        grafik1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

        # Evapotranspiration mm
        fig2 = go.Figure()

        fig2.add_trace(go.Line(x=datum, y=vgsl, name='reale Evapotranspiration von Gras über sandigem Lehm'))
        fig2.add_trace(go.Line(x=datum, y=vpgb, name='potentielle Evapotranspiration von Gras'))
        fig2.add_trace(go.Line(x=datum, y=vpgh, name='potentielle Verdunstung über Gras'))
        fig2.add_trace(go.Line(x=datum, y=vpgpm, name='potentielle Evapotranspiration über Gras nach Penman Monteith'))
        fig2.add_trace(go.Line(x=datum, y=vpmb, name='potentielle Evapotranspiration über Mais'))
        fig2.add_trace(go.Line(x=datum, y=vpzb, name='potentielle Evapotranspiration über Zuckerrüben'))
        fig2.add_trace(go.Line(x=datum, y=vgls, name='reale Evapotranspiration über Gras und lehmigen Sand'))
        fig2.add_trace(go.Line(x=datum, y=vwls, name='reale Evapotranspiration über Winterweizen und lehmigen Sand'))
        fig2.add_trace(go.Line(x=datum, y=vwsl, name='reale Evapotranspiration über Winterweizen und sandigem Lehm'))

        fig2.update_layout(title='Evapotranspiration', xaxis_title='Datum', yaxis_title='Evapotranspiration (mm)',
                           legend=dict(orientation='h', yanchor='bottom', y=-1.02, xanchor='center', x=0.5))
        grafik2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

        # Bodentemperatur °C
        fig3 = go.Figure()

        fig3.add_trace(go.Line(x=datum, y=ts05, name='mittlere Bodentemperatur unbewachsenes Bodens in 5cm Tiefe'))
        fig3.add_trace(go.Line(x=datum, y=ts10, name='mittlere Bodentemperatur unbewachsenes Bodens in 10cm Tiefe'))
        fig3.add_trace(go.Line(x=datum, y=ts20, name='mittlere Bodentemperatur unbewachsenes Bodens in 20cm Tiefe'))
        fig3.add_trace(go.Line(x=datum, y=ts50, name='mittlere Bodentemperatur unbewachsenes Bodens in 50cm Tiefe'))
        fig3.add_trace(go.Line(x=datum, y=ts100, name='mittlere Bodentemperatur unbewachsenes Bodens in 1m Tiefe'))
        fig3.add_trace(go.Line(x=datum, y=tsls05, name='mittlere Bodentemperatur bei unbewachsenen lehmigen Sand in '
                                                       '5cm Tiefe'))

        fig3.update_layout(title='Bodentemperatur', xaxis_title='Datum', yaxis_title='Bodentemperatur (°C)',
                           legend=dict(orientation='h', yanchor='bottom', y=-1.02, xanchor='center', x=0.5))
        grafik3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

        # Bodenfeuchte %nFK
        fig4 = go.Figure()

        fig4.add_trace(go.Line(x=datum, y=bf10, name='Bodenfeuchte unter Gras bei sandigem Lehm zwischen 0-10cm'))
        fig4.add_trace(go.Line(x=datum, y=bf20, name='Bodenfeuchte unter Gras bei sandigem Lehm zwischen 10-20cm'))
        fig4.add_trace(go.Line(x=datum, y=bf30, name='Bodenfeuchte unter Gras bei sandigem Lehm zwischen 20-30cm'))
        fig4.add_trace(go.Line(x=datum, y=bf40, name='Bodenfeuchte unter Gras bei sandigem Lehm zwischen 30-40cm'))
        fig4.add_trace(go.Line(x=datum, y=bf50, name='Bodenfeuchte unter Gras bei sandigem Lehm zwischen 40-50cm'))
        fig4.add_trace(go.Line(x=datum, y=bf60, name='Bodenfeuchte unter Gras bei sandigem Lehm zwischen 50-60cm'))
        fig4.add_trace(go.Line(x=datum, y=bfgsl, name='Bodenfeuchte unter Gras bei sandigem Lehm zwischen 0-60cm'))
        fig4.add_trace(go.Line(x=datum, y=bfgls, name='Bodenfeuchte unter Gras bei lehmigen Sand zwischen 0-60cm'))
        fig4.add_trace(go.Line(x=datum, y=bfwls, name='Bodenfeuchte unter Winterweizen bei lehmigen Sand '
                                                      'zwischen 0-60cm'))
        fig4.add_trace(go.Line(x=datum, y=bfwsl, name='Bodenfeuchte unter Winterweizen bei sandigem Lehm '
                                                      'zwischen 0-60cm'))

        fig4.update_layout(title='Bodenfeuchte', xaxis_title='Datum', yaxis_title='Bodenfeuchte (%nFK)',
                           legend=dict(orientation='h', yanchor='bottom', y=-1.02, xanchor='center', x=0.5))
        grafik4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

        # Frosteindringtiefe und Auftauschicht cm
        fig5 = go.Figure()

        fig5.add_trace(go.Line(x=datum, y=zfumi, name='Frosteindringtiefe am Mittag bei einem unbewachsenen Boden'))
        fig5.add_trace(go.Line(x=datum, y=ztkmi, name='Auftauschicht am Mittag unter Bestand'))
        fig5.add_trace(go.Line(x=datum, y=ztumi, name='Auftauschicht am Mittag unter unbewachsenen Boden'))

        fig5.update_layout(title='Frosteindringtiefe und Auftauschicht', xaxis_title='Datum',
                           yaxis_title='Frosteindringtiefe und Auftauschicht (cm)',
                           legend=dict(orientation='h', yanchor='bottom', y=-1.02, xanchor='center', x=0.5))
        grafik5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)

        return grafik1JSON, grafik2JSON, grafik3JSON, grafik4JSON, grafik5JSON
    else:
        return ""
    #     selected_id = 2323
    #     today = datetime.date.today()
    #     end_date_str = today.replace(day=1) + relativedelta(months=1) - relativedelta(days=1)
    #     start_date_str = today.replace(day=1)
    #
    #
    #     start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    #     end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    #
    #     datum, vgsl = get_bodenfeuchte_data(selected_id, start_date, end_date)
    #
    #     # Plotly grafiklerini oluştur
    #     fig1 = go.Figure()
    #     fig1.add_trace(go.Line(x=datum, y=vgsl, name='vgsl'))
    #
    #     # Grafik ayarlarını yap
    #     fig1.update_layout(title='Hava Durumu', xaxis_title='Datum', yaxis_title='VGSL')
    #
    #     # Grafikleri HTML olarak döndür
    #     grafik1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    #
    #     # Şablonu render et   grafik1JSON=grafik1JSON
    #     return grafik1JSON
