from flask import Flask, render_template, request, url_for, flash, redirect, session

app = Flask(__name__)
app.config['SECRET_KEY'] = open('credentials.txt', 'r').readline()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dropdown')
def dropdown():
    return render_template('dropdown.html')

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

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/questions', methods=(['GET', 'POST']))
def questions():
    if request.method == 'POST':
        firstName = request.form['first-name']
        lastName = request.form['last-name']
        email = request.form['email']
        affiliation = request.form['affiliation']
        question = request.form['question']
        
        session.pop('logged_in', None)

        if not firstName:
            flash('First Name is required!')
        elif not lastName:
            flash('Last Name is required!')
        elif not email:
            flash('Email is required!')
        elif not affiliation:
            flash('Affiliation is required!')
        elif not question:
            flash('Question is required!')  
        else:
            return redirect(url_for('questions'))
    
    return render_template('questions.html')