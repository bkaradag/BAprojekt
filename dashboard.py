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
    fig1.add_trace(go.Bar(x=datum, y=vgsl, name='vgsl'))

    # Grafik ayarlarını yap
    fig1.update_layout(title='Hava Durumu', xaxis_title='Datum', yaxis_title='VGSL')

    # Grafikleri HTML olarak döndür
    grafik1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    # Şablonu render et
    return render_template('dashboard.html', grafik1JSON=grafik1JSON)
 else:
     # istek methodu GET ise, sayfayı görüntüle
        stations = get_stations()
        return render_template('dashboard.html', stations=stations)