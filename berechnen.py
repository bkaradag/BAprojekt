import pandas as pd
from database import get_campus_wetter_data

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

    return datum_ser, temp_ser, rel_feuchte_ser,wind_gesch_ser, luft_druck_ser, luft_druck_ser, global_st_ser, strahlug_bilanz_ser, niederschlag_10m_ser, niederschlag_tag_ser, uv_index_ser, m_mw_list, j_mw_list, zj_mw_list




