# import the Flask class from the flask module
from flask import Flask, render_template,redirect, url_for, request, flash, session
from werkzeug.utils import secure_filename
#from flask_mail import Message, Mail
#import flask_login
import os
import sqlite3
import time
import pandas as pd

UPLOAD_FOLDER = '/home/ubuntu/flaskapp/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# create the application object
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = """b'y\xb2\x8b\xf9\x01\x8f\x0f*\xb7\xf8M\x85\x80v\xfb\x9f\xadGW\xba\xb4\x1d\xf7\xf8''"""
#mail = Mail(app)
#app.config.update(
#DEBUG=True,
#MAIL_SERVER = 'smtp.gmail.com',
#MAIL_PORT = 465,
#MAIL_USE_SSL = True,
#MAIL_USERNAME = 'ngundru@gmail.com',
#MAIL_PASSWORD = 'Loyola2008')

#mail = Mail(app)

#login_manager = flask_login.LoginManager()
#login_manager.init_app(app)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/index')
def index():
    return render_template('layout.html')  # render a template

@app.route('/registration',methods=['GET', 'POST'])
def registration():
    error = None
    #first build username list:
    conn = sqlite3.connect('/home/ubuntu/flaskapp/db/users.db')
    c = conn.cursor()
    df = pd.read_sql("Select * from users",conn)
    users = df['username'].tolist()
    conn.close()
    #read webform for user input
    if request.method == 'POST':
        if request.form['username'] in users:
            error = 'UserName Already Exists. Please try again.'
        elif len(request.form['password']) < 8:
            error = 'Password is too short.  Please try again.'
        else:
            #insert username and password into db
            conn = sqlite3.connect('/home/ubuntu/flaskapp/db/users.db')
            c = conn.cursor()
            now = time.strftime("%Y-%m-%d")
            c.execute("INSERT INTO users values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(request.form['username'],request.form['password'],now,request.form['practicename'],request.form['contactname'] 		   ,request.form['contactphone'] ,request.form['contactemail']    ,request.form['nodoctors']  ,request.form['nolocations']  ,request.form['MailingAddress1'] ,request.form['MailingAddress2']    ,request.form['MailingAddress3'] ,request.form['MailingAddressCity'],request.form['MailingAddressState'] ,request.form['MailingAddressZip'],request.form['BillingAddress1'],request.form['BillingAddress2'] ,request.form['BillingAddress3'] ,request.form['BillingAddressCity'] ,request.form['BillingAddressState'] 	,request.form['BillingAddressZip'] ,request.form['PracticeType'] 	  	  ,request.form['PracticeAge'],request.form['nopatients'],request.form['EstSupplySpend'] ,request.form['FiscalYearEnd'] ))
            conn.commit()
            conn.close()
            return redirect(url_for('login',error=None))
    #error = None
    return render_template('registration.html',error=error)  # render a template

@app.route('/report', methods=['GET', 'POST'])
def report():
    user=request.args.get('user')
    return render_template('report.html',user=user)#,path=path)  # render a template
    #return redirect(url_for('upload', user=user))

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect('/home/ubuntu/flaskapp/db/users.db')
    df = pd.read_sql("Select * from users",conn)
    users = df['username'].tolist()
    df.set_index("username",drop=True,inplace=True)
    passwords = df.to_dict(orient="index")
    conn.commit()
    conn.close()
    error = None
    if request.method == 'POST':
        #read db file for users and passwords
        if request.form['username'] not in users:
            error = 'UserName Does Not Exist. Please try again.'
        elif request.form['username'] in users and request.form['password'] != passwords[request.form['username']]['password']:
            error = 'Invalid Credentials. Please try again.'
        else:
            user = request.form['username']
            #session['logged_in'] = True
            #session['username'] = user
            return redirect(url_for('report', user=user))#, session=session['logged_in']))#,path=path))
	    #return render_template('upload.html',user=user)
    return render_template('login.html', error=error)  

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('homepage'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    #user=request.args.get('user')
    listoflinks = []
    user=request.args.get('user')
    #session=request.args.get('sessionid')
    #logged_in = session['logged_in']
    #if user in session and logged_in == True:
    #    supersecretmessage = 'I should see this'
    #else:
    #    supersecretmessage = 'ERROR!!!  I shouldnt see this'
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],user)) == False:
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'],user))
    mypath = os.path.join(app.config['UPLOAD_FOLDER'],user)
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    for i in range(len(onlyfiles)):
        filenamebuild = str(onlyfiles[i])
        urlbuild = url_for('uploaded_file',filename=filenamebuild,user=user)
        listoflinks.append([urlbuild,filenamebuild])
    #link = urlbuild
    if len(onlyfiles) == 0:
        link = ''
        filenamebuild = ''
        urlbuild = ''
        listoflinks = []
    link = urlbuild

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],user)) == False:
                os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'],user))
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],user, filename)) 
            flash('File Successfully Uploaded!') 
            #render_template('upload.html', files = link, names = filenamebuild, listoflinks = listoflinks)
                
    return render_template('upload.html', files = link, names = filenamebuild, listoflinks = listoflinks, user=user)#,session=session['logged_in'],sessionid=session['id'])#,supersecretmessage=supersecretmessage)

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    user=request.args.get('user')
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'],user),filename)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True, port=5050)
    
    
    
