from flask_mail import Message,Mail
import MySQLdb
from flask import Flask, render_template, request,redirect, send_from_directory , url_for,session,logging,flash
import pickle
app = Flask(__name__)
import requests
import requests
from flask import jsonify
import pdfplumber
import re
model = pickle.load(open('dia.pkl', 'rb'))
model01 = pickle.load(open('wis.pkl','rb'))
model02 = pickle.load(open('lung.pkl','rb'))
model03 = pickle.load(open('cvd.pkl','rb'))
url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"

payload = {
	"personalizations": [
		{
			"to": [{ "email": "muralibabu1729@gmail.com" }],
			"subject": "from bubble"
		}
	],
	"from": { "email": "from_bubble@example.com" },
	"content": [
		{
			"type": "text/plain",
			"value": "this is an appoinment call"
		}
	]
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "0f9ac642acmsh1d46da5f8d12b62p146304jsnc1406de9eae2",
	"X-RapidAPI-Host": "rapidprod-sendgrid-v1.p.rapidapi.com"
}
import os
import numpy as np
import mysql.connector
import matplotlib
from flask import Flask, Response
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
UPLOAD_FOLDER = 'python/static'
app = Flask(__name__, static_folder='static')
app.secret_key = 'mykey'
engine = create_engine('mysql+pymysql://root:new_password@localhost/healthsystem')
Session = sessionmaker(bind=engine)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:new_password@localhost/healthsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db1 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="new_password",
    database="healthsystem"
)
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])
from models import  db, PUser, HUser,Appointments,DUser1,DUser2,Doctor,Docfb,Feedback



def man():
    if request.method == 'POST':
        username = request.form['usermail']
        password = request.form['password']
        session['email'] = username
        session['count'] = 'pat'
        user = PUser.query.filter_by(uemail=username).first()
        session['user_name'] = user.uname
        if user and password == user.upassword:
            return render_template('index.html',count=session['count'])
        else:
            error = 'Invalid username or password'
            return render_template('pat_login.html', error=error)
    return render_template('pat_login.html')

def index():
    username = session.get('count')
    return render_template('index.html',count=username)

def doc_login():
    if request.method == 'POST':
        username = request.form['doctormail']
        password = request.form['doc_password']
        session['email'] = username
        session['count'] = 'doc'
        user = DUser1.query.filter_by(demail=username).first()
        session['doc_name'] = user.dname 
        if user and password == user.dpassword:
            return render_template('index.html',count=session['count'])
        else:
            error = 'Invalid username or password'
            return render_template('doc_login.html',error=error)
    return render_template('doc_login.html')

def register1():   
    if request.method == 'POST':
        username = session.get('email')
        db_session = Session()
        user = db_session.query(PUser).filter_by(uemail=username).first()
        db_session.close()
        key      = Fernet.generate_key()
        f        = Fernet(key)
        uheight  = f.encrypt(request.form['uheight'].encode())
        uweight  = f.encrypt(request.form['uweight'].encode())
        usurgery = f.encrypt(request.form['usurgery'].encode())
        uallergy = f.encrypt(request.form['uallergy'].encode())
        uchronic = f.encrypt(request.form['uchronic'].encode())
        ualcohol = f.encrypt(request.form['ualcohol'].encode())
        udrugs   = f.encrypt(request.form['udrug'].encode())
        utobacco = request.form['utobacco'] 
        utb      = utobacco.encode() 
        tkn    = f.encrypt(utb) 
        new_user = HUser(uemail=user.uemail, uheight=uheight,uweight=uweight,usurgery=usurgery,uallergy=uallergy,uchronic=uchronic,ualcohol=ualcohol,udrugs=udrugs,utobacco=bytes(tkn),keyid = key )
        db.session.add(new_user)
        db.session.commit()
        return render_template('pat_login.html')
    return render_template('userregister2.html')

def register():
    if request.method == 'POST':
        username = request.form['uname']
        usermail = request.form['umail']
        session['email'] = usermail
        session['count'] = 'pat'
        userphone     = request.form['uphone']
        usergender    = request.form['ugender']
        userpass  = request.form['upass']
        usercpass    = request.form['ucpass']
        userstno    = request.form['ustno']
        usercity    = request.form['ucity']
        usercountry = request.form['ucountry']
        userzip = request.form['uzip']
        userdob = request.form['udob']
        useroccupation = request.form['uoccupation']
        userstatus = request.form['ustatus']
        useremername = request.form['pemergencyname']
        useremernumber = request.form['pemergencynumber']
        useredulevel = request.form['uedulevel']
        file = request.files['upic']
        if file.filename == '':
           flash('No image selected for uploading')
           return redirect(request.url)
        if file:
           filename = secure_filename(file.filename)
           filename_variable = filename
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           new_user = PUser(uname=username, udob=userdob,ugender=usergender,uemail=usermail,udoorno=userstno,ucity=usercity,ucountry=usercountry,uzipcode=userzip,uphone=userphone,uoccupation=useroccupation,uemergencyname=useremername,uemergencynumber=useremernumber,educationlevel=useredulevel,upassword=userpass,maritalstatus=userstatus,profile_pic=filename_variable)
           db.session.add(new_user)
           db.session.commit()
           return render_template('userregister2.html')
        else:
           flash('Allowed image types are - png, jpg, jpeg, gif')
           return redirect(request.url)
 
    return render_template('userregister1.html')

def dregister():
    if request.method == 'POST':    
        dname=request.form['dname']
        demail=request.form['dmail']
        session['email'] = demail
        session['count'] = 'doc'
        dphno=request.form['dphone']
        dgender=request.form['dgender']
        ddoorno=request.form['ddrno']
        dcity=request.form['dcity']
        dcountry=request.form['dcountry']
        dspeciality=request.form['dspeciality']
        dzipcode=request.form['dzip']
        ddob=request.form['ddob']
        dpassword  = request.form['dpassword']
        doc_user=DUser1(dname=dname,demail=demail,dphno=dphno,dgender=dgender,ddoorno=ddoorno,dcity=dcity,dcountry=dcountry,dzipcode=dzipcode,ddob=ddob,dpassword=dpassword,dspeciality=dspeciality)
        db.session.add(doc_user)
        db.session.commit()
        return render_template('dregister2.html')
    return render_template('dregister.html')

def dregister2():
    if request.method == 'POST':
        drname = session.get('email')
        dheight=request.form['dheight']
        dweight=request.form['dweight']
        dedulevel=request.form['dedulevel']
        dlicensenumber=request.form['dlicensenumber']
        dexperience=request.form['dexperience']
        dpreinstitution=request.form['dpreinstitution']
        d_user=DUser2(demail=drname,dheight=dheight,dweight=dweight,dedulevel=dedulevel,dlicensenumber=dlicensenumber,dexperience=dexperience,dpreinstitution=dpreinstitution)
        db.session.add(d_user)
        db.session.commit()
        return render_template('index.html')
    return render_template('dregister2.html')

def dprofile1():
    docmail=session.get('email')
    dname  = session.get('doc_name')
    db_session=Session()
    doc=db_session.query(DUser1).filter_by(demail=docmail).first()
    doch=db_session.query(DUser2).filter_by(demail=docmail).first()
    dappt = db_session.query(Appointments).filter_by(doc_name=dname, status='accepted').all()
    db_session.close()
    return render_template('dprofile1.html',dname=doc.dname,image_name='profile.jpg',ddob=doc.ddob,dgender=doc.dgender,demail=doc.demail,ddoorno=doc.ddoorno,dcity=doc.dcity,dcountry=doc.dcountry,dzipcode=doc.dzipcode,dphno=doc.dphno,
                         demailh=doch.demail,dheighth=doch.dheight,dweighth=doch.dweight,dedulevelh=doch.dedulevel,dlicensenumberh=doch.dlicensenumber,dexperienceh=doch.dexperience,dpreinstitutionh=doch.dpreinstitution,dappt = dappt)
       
def result():
    username = session.get('email')
    db_session = Session()
    amts = db_session.query(Appointments).filter_by(mail=username).all()
    db_session.close()
    return render_template('result.html',amts=amts)

def profile():
    usermail = session.get('email')
    db_session = Session()
    user = db_session.query(PUser).filter_by(uemail=usermail).first()
    userh = db_session.query(HUser).filter_by(uemail=usermail).first()
    appointment = db_session.query(Appointments).filter_by(pat_mail=usermail).all()
    key  = userh.keyid
    f    = Fernet(key)
    tkn = userh.utobacco
    output      = f.decrypt(tkn).decode()

    db_session.close()
    return render_template('userprofile.html',name=user.uname,image_name='profile.jpg',dob=user.udob,gender=user.ugender,email=user.uemail,doorno=user.udoorno,city=user.ucity,country=user.ucountry,zipcode=user.uzipcode,phone=user.uphone,occupation=user.uoccupation,emername=user.uemergencyname,emernumber=user.uemergencynumber,education=user.educationlevel,maritalstatus=user.maritalstatus,
                           emailh=userh.uemail,heighth=f.decrypt(userh.uheight).decode(),weighth=f.decrypt(userh.uweight).decode(),allergyh=f.decrypt(userh.uallergy).decode(),chronich=f.decrypt(userh.uchronic).decode(),drugsh=f.decrypt(userh.udrugs).decode(),tobaccoh=output,surgeryh = f.decrypt(userh.usurgery).decode(),upass=user.upassword,appointment=appointment,profile_pic=user.profile_pic)

def feedback():
    if request.method == 'POST':
        usermail = session.get('email')
        useroption = request.form['option']
        if useroption == 'Doctor':
            domname = request.form['field']
            docname = request.form['docname']
        usercontent = request.form['ucontent']
        new_user = Feedback(umail=usermail,uoption=useroption,ucontent=usercontent)
        db.session.add(new_user)
        db.session.commit()
        if useroption == 'Doctor':
            db_session = Session()
            fb = db_session.query(Feedback).filter_by(umail=usermail).order_by(Feedback.uid.desc()).first()
            new_fb = Docfb(uid=fb.uid,domname=domname,docname=docname)
            db.session.add(new_fb)
            db.session.commit()

        return profile()
    return render_template('feedback.html',count=session['count'])



def get_data1():
    
        selected_table = request.args.get('selected_table')
        if selected_table == 'Doctor':
            column_values = Doctor.query.with_entities(Doctor.ddomain).distinct().all()
            column_values = [value.ddomain for value in column_values]

        return jsonify(column_values)


def get_data2(selected_value):
    attribute_values = db.session.query(Doctor.dname).filter_by(ddomain=selected_value).distinct().all()
    attribute_values = [value[0] for value in attribute_values]
    return jsonify(attribute_values)



       
def bp():
    if request.method == 'POST':
        #blood pressure
        sysbp  = request.form['sysbp']
        ideal_sysbp = 120
        user_sys = float(sysbp)
        labels = ['IDEAL','USER_LEVEL']
        values = [ideal_sysbp,user_sys]
        x_pos = [0,1]
        plt.figure(figsize=(10,5))
        plt.bar(x_pos,values,align='center',alpha=0.5)
        plt.xticks(x_pos,labels)
        plt.ylabel('SYSTOLIC BLOOD PRESSURE LEVEL')
        plt.title('ANALYSIS OF IDEAL VS USER SYSTOLIC BLOOD PRESSURE LEVEL (in mm Hg)')
        buffer1 = io.BytesIO()
        plt.savefig(buffer1, format='png')
        buffer1.seek(0)
        image_base64_1 = base64.b64encode(buffer1.read()).decode('utf-8')
        buffer1.close()
        usysbp = int(sysbp)
        diabp  = request.form['diabp']
        ideal_diabp = 80
        user_dia = float(diabp)
        labels = ['IDEAL','USER_LEVEL']
        values = [ideal_diabp,user_dia]
        x_pos = [0,1]
        plt.figure(figsize=(10,5))
        plt.bar(x_pos,values,align='center',alpha=0.5)
        plt.xticks(x_pos,labels)
        plt.ylabel('DIASTOLIC BLOOD PRESSURE LEVEL')
        plt.title('ANALYSIS OF IDEAL VS USER DIASTOLIC BLOOD PRESSURE LEVEL (in mm Hg)')
        buffer9 = io.BytesIO()
        plt.savefig(buffer9, format='png')
        buffer9.seek(0)
        image_base64_9 = base64.b64encode(buffer9.read()).decode('utf-8')
        buffer9.close()
        udiabp = int(diabp)
        return render_template('bpchart.html', image_base64_1=image_base64_1,image_base64_9=image_base64_9,usysbp=usysbp,udiabp=udiabp)
    return render_template('bp.html')  
   

def bmi():
    if request.method == 'POST':
        #bmi
        bmi = request.form['bmi']
        ideal_bmi_min = 18
        ideal_bmi_max = 25
        user_bmi = float(bmi)
        labels = ['IDEAL_MINIMUM','USER_LEVEL','IDEAL MAXIMUM']
        values = [ideal_bmi_min,user_bmi,ideal_bmi_max]
        x_pos = [0,1,2]
        plt.figure(figsize=(10,5))
        plt.bar(x_pos,values,align='center',alpha=0.5)
        plt.xticks(x_pos,labels)
        plt.ylabel('BMI LEVEL')
        plt.title('ANALYSIS OF IDEAL VS USER BMI (in kg/m2)')
        buffer5 = io.BytesIO()
        plt.savefig(buffer5, format='png')
        buffer5.seek(0)
        image_base64_5 = base64.b64encode(buffer5.read()).decode('utf-8')
        buffer5.close()
        ubmi = float(bmi)
        return render_template('bmichart.html', image_base64_5=image_base64_5,ubmi=ubmi)
    return render_template('bmi.html')  


def bs():
    if request.method == 'POST':
        #bs 
        bsugarf = request.form['bsugarfast']
        ideal_sugarf_min = 70
        ideal_sugarf_max = 100
        user_sugarf = float(bsugarf)
        labels = ['IDEAL_MINIMUM','USER_LEVEL','IDEAL MAXIMUM']
        values = [ideal_sugarf_min,user_sugarf,ideal_sugarf_max]
        x_pos = [0,1,2]
        plt.figure(figsize=(10,5))
        plt.bar(x_pos,values,align='center',alpha=0.5)
        plt.xticks(x_pos,labels)
        plt.ylabel('BLOOD SUGAR LEVEL')
        plt.title('ANALYSIS OF IDEAL VS USER BLOOD SUGAR LEVEL DURING FASTING (in mg/dL)')
        buffer2 = io.BytesIO()
        plt.savefig(buffer2, format='png')
        buffer2.seek(0)
        image_base64_2 = base64.b64encode(buffer2.read()).decode('utf-8')
        buffer2.close()
        ubsugarf = int(bsugarf)
        bsugara = request.form['bsugarate']
        ideal_sugara_min = 70
        ideal_sugara_max = 140
        user_sugara = float(bsugara)
        labels = ['IDEAL_MINIMUM','USER_LEVEL','IDEAL MAXIMUM']
        values = [ideal_sugara_min,user_sugara,ideal_sugara_max]
        x_pos = [0,1,2]
        plt.figure(figsize=(10,5))
        plt.bar(x_pos,values,align='center',alpha=0.5)
        plt.xticks(x_pos,labels)
        plt.ylabel('BLOOD SUGAR LEVEL')
        plt.title('ANALYSIS OF IDEAL VS USER BLOOD SUGAR LEVEL AFTER EATING (in mg/dL)')
        buffer10 = io.BytesIO()
        plt.savefig(buffer10, format='png')
        buffer10.seek(0)
        image_base64_10 = base64.b64encode(buffer10.read()).decode('utf-8')
        buffer2.close()
        ubsugara = int(bsugara)
        return render_template('bschart.html', image_base64_2=image_base64_2,ubsugarf=ubsugarf,image_base64_10=image_base64_10,ubsugara=ubsugara)
    return render_template('bs.html') 	


def bc():
    if request.method == 'POST': 
        #bc
        bchol = request.form['bchol']
        ideal_chol_max = 200
        user_chol = float(bchol)
        labels = ['USER_LEVEL','IDEAL MAXIMUM']
        values = [user_chol,ideal_chol_max]
        x_pos = [0,1]
        plt.figure(figsize=(10,5))
        plt.bar(x_pos,values,align='center',alpha=0.5)
        plt.xticks(x_pos,labels)
        plt.ylabel('BLOOD CHOLESTEROL LEVEL')
        plt.title('ANALYSIS OF IDEAL VS USER BLOOD CHOLESTEROL LEVEL (in mg/dL)')
        buffer3 = io.BytesIO()
        plt.savefig(buffer3, format='png')
        buffer3.seek(0)
        image_base64_3 = base64.b64encode(buffer3.read()).decode('utf-8')
        buffer3.close()
        uchol = int(bchol)
        return render_template('bcchart.html', image_base64_3=image_base64_3,uchol=uchol)
    return render_template('bc.html')


def rr():
    if request.method == 'POST': 
        #rr
        rrate = request.form['rrate']
        ideal_rate_min = 12
        ideal_rate_max = 20
        user_rate = float(rrate)
        labels = ['IDEAL_MINIMUM','USER_LEVEL','IDEAL MAXIMUM']
        values = [ideal_rate_min,user_rate,ideal_rate_max]
        x_pos = [0,1,2]
        plt.figure(figsize=(10,5))
        plt.bar(x_pos,values,align='center',alpha=0.5)
        plt.xticks(x_pos,labels)
        plt.ylabel('RESPIRATORY RATE')
        plt.title('ANALYSIS OF IDEAL VS USER RESPIRATORY RATE (in breaths/min)')
        buffer4 = io.BytesIO()
        plt.savefig(buffer4, format='png')
        buffer4.seek(0)
        image_base64_4 = base64.b64encode(buffer4.read()).decode('utf-8')
        buffer4.close()
        urr = int(rrate)
        return render_template('rrchart.html', image_base64_4=image_base64_4,urr=urr)
    return render_template('rr.html')	
		
def rbc():
    if request.method == 'POST': 
        username = session.get('email')
        db_session = Session()
        user = db_session.query(PUser).filter_by(uemail=username).first()
        
        gender = user.ugender
        print(gender)
        rbc = request.form['rbc']
        user_rbc = float(rbc)

        if gender == 'Female' or gender == 'F' :
            ideal_rbc_min = 4000000
            ideal_rbc_max = 5500000
            labels = ['IDEAL_MINIMUM','USER_LEVEL','IDEAL MAXIMUM']
            values = [ideal_rbc_min,user_rbc,ideal_rbc_max]
            x_pos = [0,1,2]
            plt.figure(figsize=(10,5))
            plt.bar(x_pos,values,align='center',alpha=0.5)
            plt.xticks(x_pos,labels)
            plt.ylabel('RBC COUNT IN FEMALE')
            plt.title('ANALYSIS OF IDEAL VS USER (FEMALE) RBC COUNT')
            buffer6 = io.BytesIO()
            plt.savefig(buffer6, format='png')
            buffer6.seek(0)
            image_base64_6 = base64.b64encode(buffer6.read()).decode('utf-8')
            buffer6.close()
            urbc = int(rbc)
            return render_template('rbcchartf.html', image_base64_6=image_base64_6,urbc=urbc,gender=gender)
        elif gender == 'Male' or gender == 'M' :
            ideal_rbc_min = 4500000
            ideal_rbc_max = 6000000
            labels = ['IDEAL_MINIMUM','USER_LEVEL','IDEAL MAXIMUM']
            values = [ideal_rbc_min,user_rbc,ideal_rbc_max]
            x_pos = [0,1,2]
            plt.figure(figsize=(10,5))
            plt.bar(x_pos,values,align='center',alpha=0.5)
            plt.xticks(x_pos,labels)
            plt.ylabel('RBC COUNT IN MALE')
            plt.title('ANALYSIS OF IDEAL VS USER (MALE) RBC COUNT') 
            buffer6 = io.BytesIO()
            plt.savefig(buffer6, format='png')
            buffer6.seek(0)
            image_base64_6 = base64.b64encode(buffer6.read()).decode('utf-8')
            buffer6.close()
            urbc = int(rbc)
            return render_template('rbcchartm.html', image_base64_6=image_base64_6,urbc=urbc,gender=gender)
    return render_template('rbc.html')	
		
		
def wbc():
    if request.method == 'POST': 
        wbc = request.form['wbc']
        ideal_wbc_min = 4000
        ideal_wbc_max = 10000
        user_wbc = float(wbc)
        labels = ['IDEAL_MINIMUM','USER_LEVEL','IDEAL MAXIMUM']
        values = [ideal_wbc_min,user_wbc,ideal_wbc_max]
        x_pos = [0,1,2]
        plt.figure(figsize=(10,5))
        plt.bar(x_pos,values,align='center',alpha=0.5)
        plt.xticks(x_pos,labels)
        plt.ylabel('WBC COUNT')
        plt.title('ANALYSIS OF IDEAL VS USER WBC COUNT')
		
        buffer7 = io.BytesIO()
        plt.savefig(buffer7, format='png')
        buffer7.seek(0)
        image_base64_7 = base64.b64encode(buffer7.read()).decode('utf-8')
        buffer7.close()
        uwbc = int(wbc)
        return render_template('wbcchart.html', image_base64_7=image_base64_7,uwbc=uwbc)
    return render_template('wbc.html')



def plat():
    if request.method == 'POST': 
        platelets = request.form['platelets']
        ideal_plat_min = 150000
        ideal_plat_max = 450000
        user_plat = float(platelets)
        labels = ['IDEAL_MINIMUM','USER_LEVEL','IDEAL MAXIMUM']
        values = [ideal_plat_min,user_plat,ideal_plat_max]
        x_pos = [0,1,2]
        plt.figure(figsize=(10,5))
        plt.bar(x_pos,values,align='center',alpha=0.5)
        plt.xticks(x_pos,labels)
        plt.ylabel('PLATELETS COUNT')
        plt.title('ANALYSIS OF IDEAL VS USER PLATELETS COUNT')	
		
        buffer8 = io.BytesIO()
        plt.savefig(buffer8, format='png')
        buffer8.seek(0)
        image_base64_8 = base64.b64encode(buffer8.read()).decode('utf-8')
        buffer8.close()
        uplat = int(platelets)
        return render_template('platchart.html',image_base64_8 =image_base64_8,uplat=uplat)
    return render_template('plat.html')
		
def button():
    return render_template('button.html') 

def home():
    return render_template('index.html')

def editdoorno():
    userdoorno = request.form['doorno']
    usermail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE puser SET udoorno = %s WHERE uemail = %s"
    values = (userdoorno, usermail)
    cursor.execute(query, values)
    db1.commit()
    return profile()

def editcity():
    usercity = request.form['city']
    usermail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE puser SET ucity = %s WHERE uemail = %s"
    values = (usercity, usermail)
    cursor.execute(query, values)
    db1.commit()
    return profile()

def editcountry():
    usercountry = request.form['country']
    usermail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE puser SET ucountry = %s WHERE uemail = %s"
    values = (usercountry, usermail)
    cursor.execute(query, values)
    db1.commit()
    return profile()

def editzipcode():
    userzipcode = request.form['zipcode']
    usermail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE puser SET uzipcode = %s WHERE uemail = %s"
    values = (userzipcode, usermail)
    cursor.execute(query, values)
    db1.commit()
    return profile()

def editphone():
    userphone = request.form['phone']
    usermail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE puser SET uphone = %s WHERE uemail = %s"
    values = (userphone, usermail)
    cursor.execute(query, values)
    db1.commit()
    return profile()

def editoccupation():
    useroccupation = request.form['occupation']
    usermail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE puser SET uoccupation = %s WHERE uemail = %s"
    values = (useroccupation, usermail)
    cursor.execute(query, values)
    db1.commit()
    return profile()

def editemername():
    useremername = request.form['emername']
    usermail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE puser SET uemergencyname = %s WHERE uemail = %s"
    values = (useremername, usermail)
    cursor.execute(query, values)
    db1.commit()
    return profile()

def editemernumber():
    useremernumber = request.form['emernumber']
    usermail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE puser SET uemergencynumber = %s WHERE uemail = %s"
    values = (useremernumber, usermail)
    cursor.execute(query, values)
    db1.commit()
    return profile()

def editeducation():
    usereducation = request.form['education']
    usermail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE puser SET educationlevel = %s WHERE uemail = %s"
    values = (usereducation, usermail)
    cursor.execute(query, values)
    db1.commit()
    return profile()

def editmaritalstatus():
    userms = request.form['ms']
    usermail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE puser SET maritalstatus = %s WHERE uemail = %s"
    values = (userms, usermail)
    cursor.execute(query, values)
    db1.commit()
    return profile()

def editpassword():
    userpassword = request.form['password']
    usermail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE puser SET upassword = %s WHERE uemail = %s"
    values = (userpassword, usermail)
    cursor.execute(query, values)
    db1.commit()
    return profile()

def deletekaro():
    usermail = session.get('email')
    cursor = db1.cursor()
    query  = "DELETE FROM puser WHERE uemail = %s"
    values = [usermail]
    cursor.execute(query,values)
    db1.commit()
    return render_template('pat_login.html')

def editddoorno():
    ddoorno = request.form['ddoorno']
    docmail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE duser1 SET ddoorno = %s WHERE demail = %s"
    values = (ddoorno, docmail)
    cursor.execute(query, values)
    db1.commit()
    return dprofile1()

def editdcity():
    doccity = request.form['dcity']
    docmail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE duser1 SET dcity = %s WHERE demail = %s"
    values = (doccity, docmail)
    cursor.execute(query, values)
    db1.commit()
    return dprofile1()

def editdcountry():
    doccountry = request.form['dcountry']
    docmail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE duser1 SET dcountry = %s WHERE demail = %s"
    values = (doccountry, docmail)
    cursor.execute(query, values)
    db1.commit()
    return dprofile1()

def editdzipcode():
    doczipcode = request.form['dzipcode']
    docmail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE duser1 SET dzipcode = %s WHERE demail = %s"
    values = (doczipcode, docmail)
    cursor.execute(query, values)
    db1.commit()
    return dprofile1()

def editdphno():
    docphone = request.form['dphno']
    docmail = session.get('email')
    cursor = db1.cursor()
    query = "UPDATE duser1 SET dphno = %s WHERE demail = %s"
    values = (docphone, docmail)
    cursor.execute(query, values)
    db1.commit()
    return dprofile1()

def ddeletekaro():
    docmail = session.get('demail')
    cursor = db1.cursor()
    query  = "DELETE FROM duser1 WHERE demail = %s"
    values = [docmail]
    cursor.execute(query,values)
    db1.commit()
    return render_template('index.html')

def search():
    if request.method == 'POST':
        name = request.form['name']
        domain = request.form['domain']
        location = request.form['location']
        if name and domain and location:
            doctors = DUser1.query.filter_by(dname=name, dcity=location).filter(DUser1.dspeciality.ilike(f'%{domain}%')).all()
        elif name and domain:
            doctors = DUser1.query.filter_by(dname=name).filter(DUser1.dspeciality.ilike(f'%{domain}%')).all()
        elif name and location:
            doctors = DUser1.query.filter_by(dname=name, dcity=location).all()
        elif domain and location:
            doctors = DUser1.query.filter(DUser1.dspeciality.ilike(f'%{domain}%'), dcity=location).all()
        elif name:
            doctors = DUser1.query.filter_by(dname=name).all()
        elif domain:
            doctors = DUser1.query.filter(DUser1.dspeciality.ilike(f'%{domain}%')).all()
        elif location:
            doctors = DUser1.query.filter_by(dcity=location).all()
        else:
            doctors = []
        return render_template('search.html', doctors=doctors)
    else:
        return render_template('search.html')


def appointment():
    if request.method == 'POST':
        pat_name = session.get('user_name')
        doc_name = request.form['doctor']
        doc_domain = request.form['domain']
        date       = request.form['date']
        time       = request.form['time']
        if doc_name == 'John Doe':
            temp = 'johndoe@example.com'
        elif doc_name == 'Emily Davis':
            temp = 'emilydavis@example.com'
        elif doc_name == 'Jane Smith':
            temp = 'janesmith@example.com'
        elif doc_name == 'Michael Wilson':
            temp = 'michaelwilson@example.com'
        elif doc_name == 'Robert Johnson':
            temp = 'robertjohnson@example.com'
        elif doc_name == 'Sarah Thompson':
            temp = 'sarahthompson@example.com'
        elif doc_name == 'Shawn':
            temp = 'Shawn@gmail.com' 
        doc_mail = temp
        pat_mail = session.get('email')
        session['doc_name'] = doc_name
        new_user = Appointments(pat_name=pat_name,pat_mail=pat_mail,doc_name=doc_name,doc_domain=doc_domain,app_date=date,mail =doc_mail,time=time)  
        db.session.add(new_user)
        db.session.commit()
        amts = Appointments.query.filter_by(pat_mail=pat_mail).all()
        return render_template('appointment.html',amts=amts)
    else:
       pat_mail = session.get('email')
       amts = Appointments.query.filter_by(pat_mail=pat_mail).all()
       if amts == None:
           return render_template('appointment.html')
       return render_template('appointment.html',amts=amts)
@app.route('/schedule')
def display1():
    pat_mail = session.get('email')
    amts = Appointments.query.filter_by(pat_mail=pat_mail).all()
    if amts == None:
        return render_template('schedule.html')
    return render_template('schedule.html',amts=amts)


def decision():
    if request.method == 'POST':
        pat_name = request.form['pat_name']
        pat_mail = session.get('email')
        decision = request.form['decision']
        count    = session.get('count')
        cursor = db1.cursor()
        if decision == 'accept':
            payload = {"personalizations": [
		                {
			"to": [{ "email": "muralibabu1729@gmail.com" }],
			"subject": "from bubble"
		                }
	                    ],
	        "from": { "email": "bubble@example.com" },
	        "content": [
	    	{
			"type": "text/plain",
			"value": "We are pleased to confirm your appointment with Dr. emilydavis at Apollo Clinic on 22/05/2023 at 6:00 pm. We appreciate your trust in our healthcare services and look forward to providing you with exceptional care."
		    }
	        ]
            }
            requests.post(url, json=payload, headers=headers)
            query = "UPDATE appointments SET status = %s WHERE pat_name = %s"
            values = ("accepted", pat_name)
            cursor.execute(query, values)
            db1.commit()
        else:
            query = "UPDATE appointments SET status = %s WHERE pat_name = %s"
            values = ("rejected",pat_name)
            cursor.execute(query,values)
            db1.commit()
        return render_template('index.html',count=count)

def visualise(param,bp,insulin,bmi,pred):
        user_value = param
        ideal_min = 80
        ideal_max = 120
        user_plat = float(param)
        labels = ['IDEAL_MINIMUM','USER_LEVEL','IDEAL MAXIMUM']
        values = [ideal_min,user_value,ideal_max]
        x_pos = [0,1,2]
        plt.figure(figsize=(10,5))
        plt.bar(x_pos,values,align='center',alpha=0.5)
        plt.xticks(x_pos,labels)
        plt.ylabel('Glucose')
        plt.title('ANALYSIS OF IDEAL VS USER  COUNT')	
		
        buffer8 = io.BytesIO()
        plt.savefig(buffer8, format='png')
        buffer8.seek(0)
        image_base64_8 = base64.b64encode(buffer8.read()).decode('utf-8')
        buffer8.close()
        uplat = int(user_plat)

        user_value1 = bp
        ideal_min1 = 90
        ideal_max1 = 140
        user_plat1 = float(bp)
        labels = ['IDEAL_MINIMUM','USER_LEVEL','IDEAL MAXIMUM']
        values = [ideal_min1,user_value1,ideal_max1]
        x_pos = [0,1,2]
        plt.figure(figsize=(10,5))
        plt.bar(x_pos,values,align='center',alpha=0.5)
        plt.xticks(x_pos,labels)
        plt.ylabel('Blood Pressure')
        plt.title('ANALYSIS OF IDEAL VS USER  COUNT')	
		
        buffer8 = io.BytesIO()
        plt.savefig(buffer8, format='png')
        buffer8.seek(0)
        image_base64_9 = base64.b64encode(buffer8.read()).decode('utf-8')
        buffer8.close()
        uplat1 = int(user_plat1)

        user_value2 = insulin
        ideal_min2 = 80
        ideal_max2 = 130
        user_plat2 = float(insulin)
        labels = ['IDEAL_MINIMUM','USER_LEVEL','IDEAL MAXIMUM']
        values = [ideal_min2,user_value2,ideal_max2]
        x_pos = [0,1,2]
        plt.figure(figsize=(10,5))
        plt.bar(x_pos,values,align='center',alpha=0.5)
        plt.xticks(x_pos,labels)
        plt.ylabel('Insulin')
        plt.title('ANALYSIS OF IDEAL VS USER  COUNT')	
		
        buffer8 = io.BytesIO()
        plt.savefig(buffer8, format='png')
        buffer8.seek(0)
        image_base64_10 = base64.b64encode(buffer8.read()).decode('utf-8')
        buffer8.close()
        uplat2 = int(user_plat2)

        user_value3 = bmi
        ideal_min3 = 19
        ideal_max3 = 25
        user_plat3 = float(bmi)
        labels = ['IDEAL_MINIMUM','USER_LEVEL','IDEAL MAXIMUM']
        values = [ideal_min3,user_value3,ideal_max3]
        x_pos = [0,1,2]
        plt.figure(figsize=(10,5))
        plt.bar(x_pos,values,align='center',alpha=0.5)
        plt.xticks(x_pos,labels)
        plt.ylabel('BMI')
        plt.title('ANALYSIS OF IDEAL VS USER  COUNT')	
		
        buffer8 = io.BytesIO()
        plt.savefig(buffer8, format='png')
        buffer8.seek(0)
        image_base64_11 = base64.b64encode(buffer8.read()).decode('utf-8')
        buffer8.close()
        uplat3 = int(user_plat3)
        return render_template('after.html',image_base64_8 =image_base64_8,image_base64_9=image_base64_9,image_base64_10=image_base64_10,image_base64_11=image_base64_11,up=uplat,up1=uplat1,up2=uplat2,up3=uplat3,data=pred)
 
def home2():
    data1 = float(request.form['a'])
    data2 = float(request.form['b'])#glucose
    data3 = float(request.form['c'])#bp
    data5 = float(request.form['e'])#insulin
    data6 = float(request.form['f'])#bmi  
    data11 = int(request.form['x'])   
    data9 = int(request.form['y'])    
    data10 = int(request.form['z'])   
    data8 = float(request.form['h'])  
    data7 = 0.1 * data11 + 0.1 * data9 + 0.1 * data10
    arr = np.array([[data1, data2, data3, data5 * 7, data6, data7, data8]])
    arr1 = arr.astype(float)
    pred = model.predict(arr1)  
    return visualise(data2,data3,data5,data6,pred)

def home1():
    data1 = request.form['a']
    data2 = request.form['b']
    data3 = request.form['c']
    data4 = request.form['d']
    data5 = request.form['e']
    data6 = request.form['f']
    data7 = request.form['g']
    data8 = request.form['h']
    data9 = request.form['i']
    data10 = request.form['j']
    data11 = request.form['k']
    arr = np.array([[data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11]])
    arr1 = arr.astype(float)
    pred = model01.predict(arr1)
    return render_template('afterwis.html',data=pred)

def home3():
    data1 = request.form['a']
    data2 = request.form['b']
    data3 = request.form['c']
    data4 = request.form['d']
    data5 = request.form['e']
    data6 = request.form['f']
    data7 = request.form['g']
    data8 = request.form['h']
    data9 = request.form['i']
    data10 = request.form['j']
    data11 = request.form['k']
    data12 = request.form['l']
    data13 = request.form['m']
    data14 = request.form['n']
    data15 = request.form['o']
    arr = np.array([[data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,data12,data13,data14,data15]])
    arr1 = arr.astype(float)
    pred = model02.predict(arr1)
    return render_template('afterlung.html',data=pred)

def cvd():
    data1 = request.form['a']
    data2 = request.form['b']
    data3 = request.form['c']
    data4 = request.form['d']
    data5 = request.form['e']
    data6 = request.form['f']
    data7 = request.form['g']
    data8 = request.form['h']
    data9 = request.form['i']
    data10 = request.form['j']
    data11 = request.form['k']
    data12 = request.form['l']
    data13 = request.form['m']
    arr = np.array([[data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,data12,data13]])
    arr1 = arr.astype(float)
    pred = model03.predict(arr1)
    return render_template('aftercvd.html',data=pred)

def model1():
    return render_template('home.html')

def model2():
    return render_template('wis.html')

def model3():
    return render_template('lung.html')

def model4():
    return render_template('cvd.html')

def upload():
    if 'pdf_file' not in request.files:
       return render_template('report_upload.html')

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
       return render_template('report_upload.html')

    if pdf_file:
        filename = pdf_file.filename
        pdf_file.save(os.path.join('python', filename))
        pdf_path = os.path.join('python',filename)
        result_string = extract_text_from_pdf(pdf_path)
        name, age, no_of_pregnancies, bp, glucose_level, insulin_level, bmi = parse_medical_report(result_string)
        return render_template('dia.html',name1=name,age1=age,np=no_of_pregnancies,bp1=bp,glucose=glucose_level,ins=float(insulin_level),bmi1=bmi)
    return render_template('report_upload.html')



def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]  
        text = page.extract_text()
        return text
    


def parse_medical_report(text):
    name_match = re.search(r'Name:\s*(\w+\s*\w+)', text)
    name = name_match.group(1) if name_match else "N/A"

    age_match = re.search(r'Age:\s*(\d+)', text)
    age = int(age_match.group(1)) if age_match else 0

    no_of_pregnancies_match = re.search(r'No\.? of Pregnancies?:\s*(\d+)', text)
    no_of_pregnancies = int(no_of_pregnancies_match.group(1)) if no_of_pregnancies_match else 0

    bp_match = re.search(r'Blood Pressure:\s*(\d+)', text) 
    bp = int(bp_match.group(1)) if bp_match else 0

    glucose_match = re.search(r'Glucose Level:\s*(\d+\.\d+)', text)
    glucose_level = float(glucose_match.group(1)) if glucose_match else 0.0

    insulin_match = re.search(r'Insulin Level:\s*(\d+\.\d+)', text)
    insulin_level = float(insulin_match.group(1)) if insulin_match else 0.0

    bmi_match = re.search(r'BMI:\s*(\d+\.\d+)', text)
    bmi = float(bmi_match.group(1)) if bmi_match else 0.0

    return name, age, no_of_pregnancies, bp, glucose_level, insulin_level,bmi



















