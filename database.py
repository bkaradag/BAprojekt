import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="", database="test")
cursor = conn.cursor()


def get_pegel_map_data():
    cursor.execute("SELECT koordinaten_pegelonline.*,pegelnummer_pegelonline.name "
                   "FROM koordinaten_pegelonline "
                   "LEFT JOIN pegelnummer_pegelonline "
                   "ON koordinaten_pegelonline.number=pegelnummer_pegelonline.number;")
    map_daten = cursor.fetchall()
    pegel = []

    for row in map_daten:
        pegel.append({'number': row[3], 'name': row[4], 'longitude': row[1], 'latitude': row[2]})
    return pegel


def get_bodenfeuchte_map_data():
    cursor.execute("SELECT bodenfeuchte_koordianten_txt.*,bodenfeuchte_stations_txt.Name "
                   "FROM bodenfeuchte_koordianten_txt "
                   "LEFT JOIN bodenfeuchte_stations_txt "
                   "ON bodenfeuchte_koordianten_txt.Stationsindex=bodenfeuchte_stations_txt.Stationsindex;")
    map_daten = cursor.fetchall()
    stations = []

    for row in map_daten:
        stations.append({'stations_index': row[1], 'breite': row[3], 'laenge': row[4], 'name': row[6]})
    return stations


def get_brightsky_map_data():
    cursor.execute("SELECT koordinaten_wmo.*, wmo_nummer.` StationName` "
                   "FROM koordinaten_wmo "
                   "LEFT JOIN wmo_nummer "
                   "ON koordinaten_wmo.`WMO-Station ID` = wmo_nummer.`WMO-Station ID`;")
    map_daten = cursor.fetchall()
    wmo_stations = []

    for row in map_daten:
        wmo_stations.append({'stations_id': row[1], 'latitude': row[2], 'longitude': row[3], 'stations_name': row[6]})
    return wmo_stations


def get_bodenfeuchte_data(selected_id, start_date, end_date):
    cursor.execute(
        f'SELECT * FROM bodenfeuchte_dwd_txt WHERE Stationsindex = {selected_id} AND Datum BETWEEN %s AND %s ORDER BY Datum ASC',
        (start_date, end_date))
    rows = cursor.fetchall()

    datum = []

    vgsl = []
    vpgb = []
    vpgh = []
    vpgpm = []
    vpmb = []
    vpzb = []
    vgls = []
    vwls = []
    vwsl = []

    ts05 = []
    ts10 = []
    ts20 = []
    ts50 = []
    ts100 = []
    tsls05 = []

    bf10 = []
    bf20 = []
    bf30 = []
    bf40 = []
    bf50 = []
    bf60 = []
    bfgsl = []
    bfgls = []
    bfwls = []
    bfwsl = []

    zfumi = []

    ztkmi = []
    ztumi = []

    for row in rows:
        # Datum
        datum.append(row[2])
        # Evapotranspiration mm
        vgsl.append(row[3])
        vpgb.append(row[4])
        vpgpm.append(row[24])
        vpgh.append(row[5])
        vpmb.append(row[25])
        vpzb.append(row[27])
        vgls.append(row[28])
        vwls.append(row[29])
        vwsl.append(row[30])
        # Bodentemperatur °C
        ts05.append(row[6])
        ts10.append(row[7])
        ts20.append(row[8])
        ts50.append(row[9])
        ts100.append(row[10])
        tsls05.append(row[20])
        # Bodenfeuchte %nFK
        bf10.append(row[12])
        bf20.append(row[13])
        bf30.append(row[14])
        bf40.append(row[15])
        bf50.append(row[16])
        bf60.append(row[17])
        bfgsl.append(row[18])
        bfgls.append(row[19])
        bfwls.append(row[31])
        bfwsl.append(row[32])
        # Frosteindringtiefe und Auftauschicht cm
        zfumi.append(row[11])
        ztkmi.append(row[22])
        ztumi.append(row[23])

    return datum, vgsl, vpgb, vpgpm, vpgh, vpmb, vpzb, vgls, vwls, vwsl, ts05, ts10, ts20, ts50, ts100, tsls05, bf10, \
           bf20, bf30, bf40, bf50, bf60, bfgls, bfgsl, bfwls, bfwsl, zfumi, ztkmi, ztumi


def get_pegel_data(selected_id, start_date, end_date):
    cursor.execute(
        f'SELECT * FROM pegelerfassung WHERE number = {selected_id} AND datum BETWEEN %s AND %s ORDER BY Datum ASC',
        (start_date, end_date))
    rows = cursor.fetchall()

    datum = []
    value = []
    wasserstand_mnw_mhw = []
    wasserstand_nsw_hsw = []

    for row in rows:
        datum.append(row[8])
        value.append(row[3])
        wasserstand_mnw_mhw.append(row[4])
        wasserstand_nsw_hsw.append(row[5])
    return datum, value, wasserstand_mnw_mhw, wasserstand_nsw_hsw


def get_campus_wetter_data():  # start_date, end_date

    cursor.execute('SELECT * FROM campuswetter_hoexter')
    # cursor.execute(f'SELECT * FROM campuswetter_hoexter Zeit(MEZ) BETWEEN %s AND %s ORDER BY Datum ASC',(start_date, end_date))
    rows = cursor.fetchall()

    datum = []
    temperatur = []
    rel_feuchte = []
    wind_gesch = []
    luft_druck = []
    global_str = []
    strahlug_bilanz = []
    niederschlag_10m = []
    niederschlag_tag = []
    uv_index = []

    for row in rows:
        datum.append(row[0])
        temperatur.append(row[1])
        rel_feuchte.append(row[2])
        wind_gesch.append(row[3])
        luft_druck.append(row[5])
        global_str.append(row[6])
        strahlug_bilanz.append(row[7])
        niederschlag_10m.append(row[8])
        niederschlag_tag.append(row[9])
        uv_index.append(row[10])

    return datum, temperatur, rel_feuchte, wind_gesch, luft_druck, global_str, strahlug_bilanz, niederschlag_10m, \
           niederschlag_tag, uv_index


def get_brightsky_wetter_data():
    cursor.execute('SELECT * FROM brightsky_wetterinformationen')
    rows = cursor.fetchall()

    datum = []
    WMO_stations = []
    niederschlag = []
    luftdruck = []
    relat_feuchte = []
    sonnenschein = []
    temp = []

    for row in rows:
        datum.append(row[7])
        WMO_stations.append(row[1])
        niederschlag.append(row[2])
        luftdruck.append(row[3])
        relat_feuchte.append(row[4])
        sonnenschein.append(row[5])
        temp.append(row[6])

    return datum, WMO_stations, niederschlag, luftdruck, relat_feuchte, sonnenschein, temp


def get_brightsky_wind_data():
    cursor.execute('SELECT * FROM brightsky_windinformationen')
    rows = cursor.fetchall()

    datum = []
    WMO_stations = []
    wind_richtung = []
    wind_geschw = []
    wind_boe_rich = []
    wind_boe_geschw = []

    for row in rows:
        datum.append(row[7])
        WMO_stations.append(row[1])
        wind_richtung.append(row[2])
        wind_geschw.append(row[3])
        wind_boe_rich.append(row[4])
        wind_boe_geschw.append(row[5])

    return datum, WMO_stations, wind_richtung, wind_geschw, wind_boe_rich, wind_boe_geschw
