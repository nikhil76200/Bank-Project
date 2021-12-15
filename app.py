
from flask_cors import cross_origin
from flask import Flask, jsonify
from models import *
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt

import datetime
from functools import wraps


from flask import Flask
from sqlalchemy.event import listen
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras
from flask import Flask,session
from app import app



app = Flask(__name__)
db = SQLAlchemy(app)



DB_HOST = "localhost"
DB_NAME = "mydata"
DB_USER = "postgres"
DB_PASS = "root"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


#=========================GET API to fetch a bank details, given branch IFSC code=========================================

@cross_origin()    
@app.route('/getdetails', methods = ['GET'])
def getdetails():
     all_mydata = []
     mydata = BankDetails.query.all()
     for bankDetails in mydata:
          results = {
                    "bank_id":bankDetails.id,
                    "bankDetails_ifsc":bankDetails.bankDetails_ifsc,
                    "bankDetails_branch":bankDetails.bankDetails_branch,
                    "bankDetails_address":bankDetails.bankDetails_address,}
          all_mydata.append(results)

     return jsonify(
            {
                "success": True,
                "mydata": all_mydata,
                "total_mydata": len(mydata),
            }
        )

#==============================GET API to fetch all details of branches, given bank name and a city=====================

@cross_origin()    
@app.route('/getbankDetails', methods = ['GET'])
def getbankDetails():
     all_mydata = []
     mydata = IndianBankDetails.query.all()
     for bankDetails in mydata:
          results = {
                    "bank_id":bankDetails.id,
                    "bankDetails_branch":bankDetails.bankDetails_branch,
                    "bankDetails_address":bankDetails.bankDetails_address,}
          all_mydata.append(results)

     return jsonify(
            {
                "success": True,
                "mydata": all_mydata,
                "total_mydata": len(mydata),
            }
        )





#==================================each API should support limit & offset parameters=================================
def q(page=0, page_size=None):
    query = session.query()
    listen(query, 'before_compile', apply_limit(page, page_size), retval=True)
    return query

def apply_limit(page, page_size):
    def wrapped(query):
        if page_size:
            query = query.limit(page_size)
            if page:
                query = query.offset(page * page_size)
        return query
    return wrapped

#=======================APIs should be authenticated using a JWT key, with validity = 5 days================================

@app.route('/register', methods=['GET', 'POST'])
def signup_user():  
 data = request.get_json()  

 hashed_password = generate_password_hash(data['password'], method='sha256')
 
 new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False) 
 db.session.add(new_user)  
 db.session.commit()    

 return jsonify({'message': 'registered successfully'})

@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
 
  auth = request.authorization   

  if not auth or not auth.username or not auth.password:  
     return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

  user = Users.query.filter_by(name=auth.username).first()   
     
  if check_password_hash(user.password, auth.password):  
     token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
     return jsonify({'token' : token.decode('UTF-8')}) 

  return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/users', methods=['GET'])
def get_all_users():  
   
   users = Users.query.all() 

   result = []   

   for user in users:   
       user_data = {}   
       user_data['public_id'] = user.public_id  
       user_data['name'] = user.name 
       user_data['password'] = user.password
       user_data['admin'] = user.admin 
       
       result.append(user_data)   

   return jsonify({'users': result})