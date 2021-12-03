from flask import Flask, render_template, request
import pandas as pd
from olympics_queries import OlympicsQueries
from pretty_html_table import build_table

app = Flask(__name__)

db_name = 'olympics'

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
    olympics_queries = OlympicsQueries(db_name)

    text = request.args.get('jsdata')
    labels = ['Bronze','Silver','Gold']
    values = olympics_queries.get_medal_count_by_country(text)

    values = [values['bronze'], values['silver'], values['gold']]

    if not values:
        error_messege = 'Country not found'
        return render_template("notFound.html", error_messege=error_messege)

    return render_template('graphs.html', text=text, labels=labels, values=values)

@app.route('/competidorMedals')
def competidorMedals():
    return render_template('competidorMedals.html')

@app.route('/findMedalsByCompetidor')
def findMedalsByCompetidor():
    olympics_queries = OlympicsQueries(db_name)

    text = request.args.get('jsdata')
    labels = ['Bronze','Silver','Gold']
    values = olympics_queries.get_medal_count_by_competitor(text)

    values = [values['bronze'], values['silver'], values['gold']]

    if not values:
        error_messege = 'Competidor not found'
        return render_template("notFound.html", error_messege=error_messege)

    return render_template('graphs.html', text=text, labels=labels, values=values)


@app.route('/top_10_countries')
def top_10_countries():
    olympics_queries = OlympicsQueries(db_name)

    panda_table_html = build_table(olympics_queries.get_country_top_10_with_soceconomic_markers(), 'blue_light', 
                                   index=True,)
    text_file = open("./templates/tablesRender.html", "w")
    text_file.write(panda_table_html)
    text_file.close()

    return render_template('tablesRender.html')
