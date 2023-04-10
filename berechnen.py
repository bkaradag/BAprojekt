import pandas as pd
from database import get_campus_wetter_data, get_brightsky_wetter_data, get_brightsky_wind_data


def berechnen_campus_wetter_daten():

    campus_data = get_campus_wetter_data()

    datum_ser = pd.Series(campus_data[0])
    temp_ser = pd.Series(campus_data[1])
    rel_feuchte_ser = pd.Series(campus_data[2])
    wind_gesch_ser = pd.Series(campus_data[3])
    luft_druck_ser = pd.Series(campus_data[4])
    global_st_ser = pd.Series(campus_data[5])
    strahlug_bilanz_ser = pd.Series(campus_data[6])
    niederschlag_10m_ser = pd.Series(campus_data[7])
    niederschlag_tag_ser = pd.Series(campus_data[8])
    uv_index_ser = pd.Series(campus_data[9])

    series = [pd.Series(campus_data[i], index=pd.to_datetime(datum_ser)) for i in range(1, len(campus_data))]

    m_mw_list = [mw.resample('M').mean() for mw in series]
    j_mw_list = [mw.resample('Y').mean() for mw in series]
    zj_mw_list = [mw.resample('10Y').mean() for mw in series]

    return datum_ser, temp_ser, rel_feuchte_ser,wind_gesch_ser, luft_druck_ser, luft_druck_ser, \
           global_st_ser, strahlug_bilanz_ser, niederschlag_10m_ser, niederschlag_tag_ser, uv_index_ser, \
           m_mw_list, j_mw_list, zj_mw_list

def berechnen_brightsky_wetter_daten():

    brightsky_wetter_daten = get_brightsky_wetter_data()

    datum_ser = pd.Series(brightsky_wetter_daten[0])
    niederschlag_ser = pd.Series(brightsky_wetter_daten[1])
    luftdruck_ser = pd.Series(brightsky_wetter_daten[2])
    relat_feuchte_ser = pd.Series(brightsky_wetter_daten[3])
    sonnenschein_ser = pd.Series(brightsky_wetter_daten[4])
    temp_ser = pd.Series(brightsky_wetter_daten[5])

    series = [pd.Series(brightsky_wetter_daten[i],
                        index=pd.to_datetime(datum_ser)) for i in range(1, len(brightsky_wetter_daten))]

    m_mw_list = [mw.resample('M').mean() for mw in series]
    j_mw_list = [mw.resample('Y').mean() for mw in series]
    zj_mw_list = [mw.resample('10Y').mean() for mw in series]

    return datum_ser, niederschlag_ser, luftdruck_ser, relat_feuchte_ser, sonnenschein_ser, temp_ser, m_mw_list, \
           j_mw_list, zj_mw_list

def berechnen_brightsky_wind_daten():

    brightsky_wind_daten = get_brightsky_wind_data()

    datum_ser = pd.Series(brightsky_wind_daten[0])
    wind_richtung_ser = pd.Series(brightsky_wind_daten[1])
    wind_geschw_ser = pd.Series(brightsky_wind_daten[2])
    wind_boe_rich_ser = pd.Series(brightsky_wind_daten[3])
    wind_boe_geschw_ser = pd.Series(brightsky_wind_daten[4])

    series = [pd.Series(brightsky_wind_daten[i],
                        index=pd.to_datetime(datum_ser)) for i in range(1, len(brightsky_wind_daten))]

    m_mw_list = [mw.resample('M').mean() for mw in series]
    j_mw_list = [mw.resample('Y').mean() for mw in series]
    zj_mw_list = [mw.resample('10Y').mean() for mw in series]

    return datum_ser, wind_richtung_ser, wind_geschw_ser, wind_boe_rich_ser, wind_boe_geschw_ser, m_mw_list, \
           j_mw_list, zj_mw_list




