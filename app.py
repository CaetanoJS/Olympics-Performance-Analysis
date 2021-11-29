from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route('/mixedGraphs')
def mixedGraphs():
    return render_template('mixedGraphs.html')

@app.route('/graphByCountry')
def graphByCountry():
    return render_template('graphByCountry.html')

@app.route('/findByCountry')
def findByCountry():
    text = request.args.get('jsdata')
    label = []
    value = []
    return render_template('graphs.html', text=text, label=label, value=value)