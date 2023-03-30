import pandas as pd
from database import get_campus_wetter_data

def berechnen_campus_wetter_daten():

    campus_data = get_campus_wetter_data()

    datum_ser = pd.Series(campus_data[0])
    temp_ser = pd.Series(campus_data[1])

    series = [pd.Series(campus_data[i], index=pd.to_datetime(datum_ser)) for i in range(1, len(campus_data))]

    m_mw_list = [mw.resample('M').mean() for mw in series]
    j_mw_list = [mw.resample('Y').mean() for mw in series]
    zj_mw_list = [mw.resample('10Y').mean() for mw in series]

    return datum_ser,temp_ser



