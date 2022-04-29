from flask import Flask, render_template, request, url_for, flash, redirect, session
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
credentials = open('credentials.txt', 'r')
app.config['SECRET_KEY'] = credentials.readline()
email_password = credentials.readline()

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/dropdown')
# def dropdown():
#     return render_template('dropdown.html')

@app.route('/alz')
def alz():
    return render_template('alz.html')

@app.route('/alz_pre_vs_post')
def alz_pre_post():
    return render_template('alz_pre_vs_post.html')

@app.route('/als-current')
def als_current():
    return render_template('als-current.html')

@app.route('/als-past')
def als_past():
    return render_template('als-past.html')

@app.route('/ac-questions')
def ac_questions():
    return render_template('ac-questions.html')

# @app.route('/team')
# def team():
#     return render_template('team.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/pastchoropleth')
def pastchoropleth():
    return render_template('pastchoropleth.html')

@app.route('/currentchoropleth')
def currentchoropleth():
    return render_template('currentchoropleth.html')

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
            port_number = 587
            msg = MIMEMultipart()
            msg['From'] = 'socialmediafamilycaregivingresearch@gmx.com'
            msg['To'] = 'socialmediafamilycaregivingresearch@gmx.com'
            msg['Subject'] = 'SocialMediaFamilyCaregivingResearch Question'
            message = 'First Name: ' + firstName + '\n' +\
                'Last Name: ' + lastName + '\n' +\
                'Email: ' + email + '\n' +\
                'Affiliation: ' + affiliation + '\n' +\
                'Question: ' + question
            msg.attach(MIMEText(message))
            try:
                mailserver = smtplib.SMTP('smtp.gmx.com',port_number)
                mailserver.ehlo()
                mailserver.starttls()
                mailserver.login("socialmediafamilycaregivingresearch@gmx.com", email_password)
                mailserver.sendmail('socialmediafamilycaregivingresearch@gmx.com','socialmediafamilycaregivingresearch@gmx.com',msg.as_string())
                mailserver.quit()
                flash("Question submitted successfully!")
            except:
                flash("Message failed to send!")
            
            return redirect(url_for('questions'))
    
    return render_template('questions.html')