import json
from datetime import datetime

import plotly
import plotly.graph_objs as go
from dateutil.relativedelta import relativedelta
from flask import render_template, request

from database import get_pegel_data, get_pegel_map_data


def get_pegel():
    if request.method == 'POST':
        # HTML formundan seçilen istasyon ID'si alınır
        selected_id = request.form.get('pegel')
        if not selected_id:
            return "Ein Pegel auswaehlen."

        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')

        if not (start_date_str and end_date_str):
            return "Zeitraum auswaehlen."
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        datum, value, wasserstand_nsw_hsw, wasserstand_mnw_mhw = get_pegel_data(selected_id, start_date, end_date)

        farbe_wstand = {'normal': 'blue', 'low': 'red', 'high': 'green', 'commented':'grey','unknown':'black'}
        farben = [farbe_wstand[s] for s in wasserstand_nsw_hsw]


        fig1 = go.Figure()
        fig1.add_trace(go.Line(x=datum, y=value, name='value',line=dict(color=farben)))
        fig1.update_layout(title='Pegel', xaxis_title='Datum', yaxis_title='Value')
        grafik1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('pegel.html', grafik1JSON=grafik1JSON)
    else:
        pegel = get_pegel_map_data()
        return render_template('pegel.html', pegel=pegel)

