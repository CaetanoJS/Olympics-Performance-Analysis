from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route('/graphs')
def graphs():
    text = request.args.get('jsdata')

    if text == 'sss':
        suggestions_list = ['teste', '2']
    else:
        suggestions_list = ['caetano', 'PDE']
    
    return render_template('graphs.html', suggestions=suggestions_list)

@app.route('/mixedGraphs')
def mixedGraphs():
    
    return render_template('mixedGraphs.html')