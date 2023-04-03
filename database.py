import pymysql


conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="", database="test")
cursor = conn.cursor()


# istasyon secimi icin grafik olusturmada
def get_stationen_bodenfeuchte():

    cursor.execute('SELECT * FROM bodenfeuchte_stations_txt')
    rows = cursor.fetchall()

    stations = []

    for row in rows:
        stations.append({'Stationsindex': row[0], 'Name': row[1]})
    return stations

def get_pegel_nummer():

    cursor.execute('SELECT * FROM pegelnummer_pegelonline')
    rows = cursor.fetchall()

    pegel = []

    for row in rows:
        pegel.append({'number': row[0], 'name': row[1]})
    return pegel

def get_wmo_nummer():

    cursor.execute('SELECT * FROM wmo_nummer')
    rows = cursor.fetchall()

    wmo = []

    for row in rows:
        wmo.append({'WMO-Station ID': row[0], 'StationName': row[1]})
    return wmo


def get_map_daten():

    cursor.execute("SELECT Stationsindex, Breite, Länge FROM bodenfeuchte_koordianten_txt")
    map_daten = cursor.fetchall()
    return map_daten


# secilen zaman araligindaki degerleri grafiksel olarak gösterir.
def get_bodenfeuchte_data(selected_id, start_date, end_date):

    cursor.execute(
        f'SELECT * FROM bodenfeuchte_dwd_txt WHERE Stationsindex = {selected_id} AND Datum BETWEEN %s AND %s ORDER BY Datum ASC',
        (start_date, end_date))
    rows = cursor.fetchall()

    datum = []
    vgsl = []

    for row in rows:
        datum.append(row[2])
        vgsl.append(row[3])
    return datum, vgsl

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

    return datum, temperatur, rel_feuchte, wind_gesch, luft_druck, global_str, strahlug_bilanz, niederschlag_10m, niederschlag_tag, uv_index

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
