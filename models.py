from app import db
from sqlalchemy.dialects.postgresql import JSON
from flask import Flask, request, jsonify, make_response
from functools import wraps
from app import app
from flask_jwt import jwt




class BankDetails(db.Model):
    __tablename__ = 'mydata'
    bank_id = db.Column(db.Integer, primary_key = True)
    ifsc = db. Column(db.String(100), nullable = False)
    branch = db.Column(db.String(100), nullable = False)
    address = db.Column(db.String(100), nullable = False)

    def __init__(self, bank_id, ifsc, branch,address):
        self.bank_id = bank_id
        self.ifsc = ifsc
        self.branch = branch
        self.address=address

    def __repr__(self):
        return "<bankDetails %r>" % self.bank_id



class IndianBankDetails(db.Model):
    __tablename__ = 'mydata'
    bank_id = db.Column(db.Integer, primary_key = True)
    branch = db.Column(db.String(100), nullable = False)
    address = db.Column(db.String(100), nullable = False)

    def __init__(self, bank_id, branch,address):
        self.bank_id = bank_id
        self.branch = branch
        self.address=address



    def __repr__(self):
        return "<IndianBankDetails %r>" % self.bank_id


class Users(db.Model):
    
     id = db.Column(db.Integer, primary_key=True)
     public_id = db.Column(db.Integer)
     name = db.Column(db.String(50))
     password = db.Column(db.String(50))
     admin = db.Column(db.Boolean)

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      token = None

      if 'x-access-tokens' in request.headers:
         token = request.headers['x-access-tokens']

      if not token:
         return jsonify({'message': 'a valid token is missing'})

      try:
         data = jwt.decode(token, app.config['\xcb\x8d\xf6\xcc\x9a\x87\x17\xeeli\x05\xa4xD\xf0x\x9d\x0e\x98:9\xad\xd0!'])
         current_user = Users.query.filter_by(public_id=data['public_id']).first()
      except:
        return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
   return decorator