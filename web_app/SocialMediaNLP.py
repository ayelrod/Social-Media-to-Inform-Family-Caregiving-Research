from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alz')
def alz():
    return render_template('alz.html')

@app.route('/als-current')
def als_current():
    return render_template('als-current.html')

@app.route('/als-past')
def als_past():
    return render_template('als-past.html')

@app.route('/team')
def team():
    return render_template('team.html')