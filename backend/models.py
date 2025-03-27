from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.dialects.sqlite import JSON 


db=SQLAlchemy()


class User(db.Model):
    __tablename__="user"
    username=db.Column(db.String,primary_key=True)
    password=db.Column(db.String,nullable=False)
    role=db.Column(db.Integer,nullable=False)
    
    
class Customer(db.Model):
    __tablename__="customer"
    cust_id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.Integer,db.ForeignKey("user.username"),nullable=False,unique=True)
    fname=db.Column(db.String,nullable=False)
    lname=db.Column(db.String,nullable=False)
    address=db.Column(db.String,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    phone=db.Column(db.Integer,nullable=False)
    jdate=db.Column(db.DateTime,nullable=False)
    action=db.Column(db.String,nullable=False)
    avg_cust_rating=db.Column(db.Integer,nullable=True)
    requests=db.relationship("Service_Requests",cascade="all,delete",backref="customer")

    
    
class Professional(db.Model):
    __tablename__="professional"
    prof_id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.Integer,db.ForeignKey("user.username"),nullable=False,unique=True)
    serv_id=db.Column(db.Integer,db.ForeignKey("services.serv_id"),nullable=False)
    fname=db.Column(db.String,nullable=False)
    lname=db.Column(db.String,nullable=False)
    exp=db.Column(db.Integer,nullable=False)
    docs=db.Column(db.String,nullable=False)
    address=db.Column(db.String,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    phone=db.Column(db.Integer,nullable=False)
    action=db.Column(db.String,nullable=False,default="False")
    avg_prof_rating=db.Column(db.Integer,nullable=True)
    requests=db.relationship("Service_Requests",cascade="all,delete",backref="professional")


class Services(db.Model):
    __tablename__="services"
    serv_id=db.Column(db.Integer,primary_key=True)
    servexp=db.Column(db.String,nullable=False,unique=True)
    description=db.Column(db.String,nullable=False)
    base_price=db.Column(db.Float,nullable=False)
    professionals=db.relationship("Professional",cascade="all,delete",backref="services")
    service_history=db.relationship("Service_Requests",cascade="all,delete",backref="services")


class Service_Requests(db.Model):
    __tablename__="service_requests"
    request_id=db.Column(db.Integer,primary_key=True)
    serv_id=db.Column(db.Integer,db.ForeignKey("services.serv_id"),nullable=False)
    prof_id=db.Column(db.Integer,db.ForeignKey("professional.prof_id"),nullable=True)
    cust_id=db.Column(db.Integer,db.ForeignKey("customer.cust_id"),nullable=False)
    rdate=db.Column(db.DateTime,nullable=False)
    cdate=db.Column(db.DateTime,nullable=True)
    base_price=db.Column(db.Float,nullable=False)
    action=db.Column(db.String,nullable=False)
    serv_rating=db.Column(db.Integer,nullable=True)
    serv_review=db.Column(db.String,nullable=True)
    cust_rating=db.Column(db.Integer,nullable=True)
    req_rejected=db.Column(JSON,default=[])