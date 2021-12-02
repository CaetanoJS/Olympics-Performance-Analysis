from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route('/mixedGraphs')
def mixedGraphs():
    return render_template('mixedGraphs.html')

@app.route('/countryMedals')
def countryMedals():
    return render_template('countryMedals.html')

@app.route('/findMedalsByCountry')
def findByCountry():
    text = request.args.get('jsdata')
    labels = ['Bronze','Silver','Gold']
    values = []

    if not values:
        error_messege = 'Country not found'
        return render_template("notFound.html", error_messege=error_messege)

    return render_template('graphs.html', text=text, labels=labels, values=values)

@app.route('/competidorMedals')
def competidorMedals():
    return render_template('competidorMedals.html')

@app.route('/findMedalsByCompetidor')
def findMedalsByCompetidor():
    text = request.args.get('jsdata')
    labels = ['Bronze','Silver','Gold']
    values = []

    if not values:
        error_messege = 'Competidor not found'
        return render_template("notFound.html", error_messege=error_messege)

    return render_template('graphs.html', text=text, labels=labels, values=values)


@app.route('/top_10_countries')
def top_10_countries():
    #panda.dataframe
    panda_table_html = [] #method call

    return render_template('top_10_countries.html', panda_table_html=panda_table_html)
