from flask import Flask, render_template, request, url_for, flash, redirect, session
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pymongo import MongoClient

app = Flask(__name__)
credentials = open('credentials.txt', 'r')
app.config['SECRET_KEY'] = credentials.readline()
email_password = credentials.readline()
CONNECTION_STRING = credentials.readline()

client = MongoClient(CONNECTION_STRING)
db = client['SocialMediaCaregivingResearch']
alz = db.AlzConnected

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

@app.route('/als-current_pre_vs_post')
def als_current_pre_post():
    return render_template('als-current_pre_vs_post.html')

@app.route('/als-past')
def als_past():
    return render_template('als-past.html')

@app.route('/als-past_pre_vs_post')
def als_past_pre_post():
    return render_template('als-past_pre_vs_post.html')

@app.route('/ac-questions')
def ac_questions():
    return render_template('ac-questions.html')

@app.route('/ac-discussions')
def ac_discussions():
    return render_template('ac-discussions.html')

@app.route('/ac')
def ac():
    return render_template('ac.html')

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

@app.route('/reddit')
def reddit():
    return render_template('reddit.html')

@app.route('/labeling', methods=(['GET', 'POST']))
def labeling():
    if not session.get("initials"):
        session["initials"] = ""
    session.pop('logged_in', None)
    unlabeled_post = db.AlzConnected.find({ "support_type": "" })[0]
    post_id = unlabeled_post["_id"]
    if request.method == 'POST':
        initials = request.form["initials"].upper()
        if not initials or initials == "None":
            flash("Initials required!")
        elif len(initials) > 3 or not initials.isalnum():
            flash("Invalid initials!") 
        else:
            session["initials"] = initials
            support_type = request.form['support']
            db.AlzConnected.update_one({"_id": post_id} , { "$set" : {"support_type": support_type}})
            db.AlzConnected.update_one({"_id": post_id} , { "$set" : {"labeled_by": initials}})
            return redirect(url_for('labeling'))

    return render_template('labeling.html', body=unlabeled_post["body"], title=unlabeled_post["title"], initials=session["initials"])

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
            msg['From'] = 'socialmediafamilycaregivingresearch@outlook.com'
            msg['To'] = 'socialmediafamilycaregivingresearch@outlook.com'
            msg['Subject'] = 'SocialMediaFamilyCaregivingResearch Question'
            message = 'First Name: ' + firstName + '\n' +\
                'Last Name: ' + lastName + '\n' +\
                'Email: ' + email + '\n' +\
                'Affiliation: ' + affiliation + '\n' +\
                'Question: ' + question
            msg.attach(MIMEText(message))
            try:
                mailserver = smtplib.SMTP('smtp-mail.outlook.com',port_number)
                mailserver.ehlo()
                mailserver.starttls()
                mailserver.login("socialmediafamilycaregivingresearch@outlook.com", email_password)
                mailserver.sendmail('socialmediafamilycaregivingresearch@outlook.com','socialmediafamilycaregivingresearch@outlook.com',msg.as_string())
                mailserver.quit()
                flash("Question submitted successfully!")
            except:
                flash("Message failed to send!")
            
            return redirect(url_for('questions'))
    
    return render_template('questions.html')