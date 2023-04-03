from flask import Flask, render_template
from bodenfeuchte import get_bodenfeuchte
from brightskywetter import get_brightsky_wetter
from brightskywind import get_brightsky_wind
from campuswetter import get_campuswetter
from map import get_map
from pegel import get_pegel

app = Flask(__name__)
app.config.suppress_callback_exceptions = True


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stations')
def map():
    return get_map()

@app.route('/bodenfeuchte', methods=['GET', 'POST'])
def bodenfeuchte():
    return get_bodenfeuchte()

@app.route('/pegel', methods=['GET', 'POST'])
def pegel():
    return get_pegel()


@app.route('/campuswetterhoexter', methods=['GET', 'POST'])
def campuswetter():
    return get_campuswetter()


@app.route('/brightsky_wetter', methods=['GET', 'POST'])
def brightsky_wetter():
    return get_brightsky_wetter()


@app.route('/brightsky_wind', methods=['GET', 'POST'])
def brightsky_wind():
    return get_brightsky_wind()


if __name__ == '__main__':
    app.run(debug=True)
