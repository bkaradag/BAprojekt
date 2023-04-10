from flask import Flask, render_template, request

from bodenfeuchte import get_bodenfeuchte
from campuswetter import get_campuswetter
from database import get_bodenfeuchte_map_data, get_pegel_map_data, get_brightsky_map_data


app = Flask(__name__)
app.config.suppress_callback_exceptions = True


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/bodenfeuchte', methods=['GET', 'POST'])
def bodenfeuchte():
    stations = get_bodenfeuchte_map_data()
    grafik1JSON, grafik2JSON, grafik3JSON, grafik4JSON, grafik5JSON = get_bodenfeuchte()  # TODO: burda bir sorun var sayfa degistirirken hata veriyor.
    if request.method != 'POST':
        return render_template('bodenfeuchte.html', stations=stations, grafik1JSON="")
    else:
        return render_template('bodenfeuchte.html', stations=stations, grafik1JSON=grafik1JSON,
                               grafik2JSON=grafik2JSON, grafik3JSON=grafik3JSON, grafik4JSON=grafik4JSON,
                               grafik5JSON=grafik5JSON)


@app.route('/pegel', methods=['GET', 'POST'])
def pegel():
    pegel = get_pegel_map_data()
    return render_template('pegel.html', pegel=pegel)


@app.route('/campuswetterhoexter', methods=['GET', 'POST'])
def campuswetter():
    return get_campuswetter()


@app.route('/brightskywetter', methods=['GET', 'POST'])
def brightsky_wetter():
    wmo_stations = get_brightsky_map_data()
    return render_template('brightskywetter.html', wmo_stations=wmo_stations)


@app.route('/brightskywind', methods=['GET', 'POST'])
def brightsky_wind():
    wmo_stations = get_brightsky_map_data()
    return render_template('brightskywind.html', wmo_stations=wmo_stations)


if __name__ == '__main__':
    app.run(debug=True)
