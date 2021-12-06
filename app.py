from re import template
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


@app.route('/top10CountriesWithIndex')
def top10CountriesWithIndex():
    olympics_queries = OlympicsQueries(db_name)

    panda_table_html = build_table(olympics_queries.get_country_top_10_with_soceconomic_markers(), 'blue_light', 
                                   index=True,)
    text_file = open("./templates/tablesRender.html", "w")
    text_file.write(panda_table_html)
    text_file.close()

    return render_template('tablesRender.html')

@app.route('/top10MedalistByCountry')
def top10MedalistByCountry():
    
    return render_template('top10MedalistByCountry.html')

@app.route('/findMedalistByCountry')
def findMedalistByCountry():
    text = request.args.get('jsdata')
    olympics_queries = OlympicsQueries(db_name)

    panda_table_html = build_table(olympics_queries.get_top_medalists_df(text), 
                                   'blue_light', 
                                   index=True,)
    text_file = open("./templates/tablesRender.html", "w")
    text_file.write(panda_table_html)
    text_file.close()

    return render_template('tablesRender.html')

@app.route('/top10BestCountries')
def top10BestCountries():
    olympics_queries = OlympicsQueries(db_name)

    panda_table_html = build_table(olympics_queries.get_countries_with_most_medals_df(10), 
                                   'blue_light', 
                                   index=True,)
    text_file = open("./templates/tablesRender.html", "w")
    text_file.write(panda_table_html)
    text_file.close()

    return render_template('tablesRender.html')

@app.route('/topCountriesLowSocialEconomicIndex')
def topCountriesLowSocialEconomicIndex():
    olympics_queries = OlympicsQueries(db_name)

    index = request.args.get('jsdata')

    if index == 'IDH':
        panda_table_html = build_table(olympics_queries.get_no_medal_worst_hdi(), 
                                       'blue_light', 
                                       index=True,) #IDH
    else:
        panda_table_html = build_table(olympics_queries.get_no_medal_worst_gdp(), 
                                       'blue_light', 
                                       index=True,) #GDP

    text_file = open("./templates/tablesRender.html", "w")
    text_file.write(panda_table_html)
    text_file.close()

    return render_template('tablesRender.html')

@app.route('/topCountriesHighSocialEconomicIndex')
def topCountriesHighSocialEconomicIndex():
    olympics_queries = OlympicsQueries(db_name)

    index = request.args.get('jsdata')

    if index == 'IDH':
        panda_table_html = build_table(olympics_queries.get_no_medal_best_hdi(), 
                                       'blue_light', 
                                       index=True,) #IDH
    else:
        panda_table_html = build_table(olympics_queries.get_no_medal_best_gdp(), 
                                       'blue_light', 
                                       index=True,) #GDP

    text_file = open("./templates/tablesRender.html", "w")
    text_file.write(panda_table_html)
    text_file.close()

    return render_template('tablesRender.html',)

@app.route('/idhGdpPerformance')
def idhGdpPerformance():
    olympics_queries = OlympicsQueries(db_name)

    text = ''
    index = request.args.get('jsdata')

    hdi_data, hdi_labels, gdp_data, gdp_labels = olympics_queries.get_med_count_soceconomics_scatter_plot()

    if index == 'IDH':
        values = hdi_data #IDH
        labels = hdi_labels
    else:
        values = gdp_data #GDP
        labels = gdp_labels

    return render_template('scatterGraph.html', text=text, values=values, labels=labels, index=index)