import json
import pandas as pd
from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
import pickle
import numpy as np
from flask_cors import CORS,cross_origin
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import csv
from csv import writer
p=11513



app=Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='db'
mysql=MySQL(app)

@app.route('/login',methods=['GET' ,'POST' ])
def login():
        msg=''
        if request.method=='POST' and 'username' in request.form and 'password' in request.form:
            print('alo itha pn')
            username=request.form['username']
            password=request.form['password']
            print(username,password)
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WhERE  username=%s and password =%s',(username,password))
            account=cursor.fetchone()
            if account:
                print("YEs Connected!")
                session['loggedin']=True
                session['id']=account['id']
                session['password']=account['password']
                return redirect(url_for('admin'))
            else:
                msg='Incorrect username/password!'            
        return render_template('Login.html',msg=msg)

@app.route('/admin',methods=['POST','GET'])
def admin():
    data=pd.read_csv( 'Cleaned_data.csv')
    locations=sorted(data['site_location'].unique())
    if request.method=='POST':
        location=request.form['location']
        bhk=request.form['bhk']
        price=request.form['price']
        bath=request.form['bath']
        sqft=request.form['sqft']
        
        row_wise=[]
        input_file = open("Cleaned_data.csv","r+")
        reader_file = csv.reader(input_file)
        value = len(list(reader_file))
        value+=14
        input_file.close()
        row_wise.append(value+1)
        row_wise.append(sqft)
        row_wise.append(bath)
        row_wise.append(price)
        row_wise.append(location)
        row_wise.append(bhk)
        
        
        with open('Cleaned_data.csv', 'a') as f_object:
 
          writer_object = writer(f_object)
          writer_object.writerow(row_wise)
          f_object.close()
        
        
        
           
    return render_template('admin.html',locations=locations)

@app.route('/features',methods=['POST','GET'])
def features():
    # x, y,a,b = np.loadtxt('Cleaned_dat a.csv', unpack=True,  skiprows=1, delimiter=',')
    data=pd.read_csv('Cleaned_data.csv')
    labels=data['bhk'].unique()
    values=data['price']
    labels1=data['total_sqft']
    # values=data['price']
    return render_template("features.html",labels1=labels1.tolist(),labels=labels.tolist(),values=values.tolist(),)

@app.route('/')
def index():
    data=pd.read_csv( 'Cleaned_data.csv')
    locations=sorted(data['site_location'].unique())
    return render_template('index.html',locations=locations)


@app.route('/predict',methods=['POST'])
def predict():
    site_location=request.form.get('location')
    bhk=request.form.get('bhk')
    bath=request.form.get('bath')
    total_sqft=request.form.get('sqft')
    pipe=pickle.load(open('RidgeModel.pkl', 'rb'))  
    print(site_location,bhk,bath,total_sqft)
    input=pd.DataFrame([[site_location,total_sqft,bath,bhk]],columns=['site_location','total_sqft','bath','bhk'])
    prediction=pipe.predict(input)[0]*1e5
    
    print(prediction)
    return str(np.round(prediction,0))
    # return ""
    
    
@app.route('/view',methods=['POST','GET'])
def view():
    # converting csv to html
    data = pd.read_csv('Cleaned_data.csv')
    return render_template('view.html', tables=[data.to_html()], titles=[''])
if __name__=="__main__":
    app.run(debug=True,port=5001)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  # data=pd.read_csv('Cleaned_data.csv')
    # labels=[row[1] for row in data]
    # values=[row[2] for row in data]   
    
    
    
    
    
    # def Login():
    
#     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     if cur==None:
        
#         print("connection not established")
     
#     fname=request.form.get('fname')
#     femail=request.form.get('email')
#     fpassword=request.form.get('password')
     
#     cur.execute("select * from tbl_user  where name=%s and email=%s and password=%s",(fname,femail,fpassword))
#     account=cur.fetchone()
#     if account:
#             # Create session data, we can access this data in other routes
#             session['loggedin'] = True
            
#             session['username'] = account['username']
#             # Redirect to home page
#             return 'Logged in successfully!'
#     cur.close()
#     return render_template('Login.html')



# @app.route('/check')
# def check():
#     conn=mysql.connector.connect("host=remotemysql.com   ")
    
 
