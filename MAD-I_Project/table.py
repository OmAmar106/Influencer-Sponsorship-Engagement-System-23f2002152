from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()
class Sponsors(db.Model):
    __tablename__ = 'sponsors'
    ID = db.Column(db.Integer,primary_key = True,autoincrement = True)
    username = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    companyname = db.Column(db.String,nullable=False)
    industry = db.Column(db.String,nullable=False)
    budget = db.Column(db.Integer,nullable=False)

class Influencer(db.Model):
    __tablename__ = 'influencer'
    ID = db.Column(db.Integer,primary_key = True,autoincrement = True)
    username = db.Column(db.String,nullable = False,unique = True)
    password = db.Column(db.String,nullable = False)
    name = db.Column(db.String,nullable = False)
    category = db.Column(db.String,nullable = False)  
    reach = db.Column(db.Integer,nullable = False)
    niche = db.Column(db.String)

class Campaign(db.Model):
    __tablename__ = 'campaign'
    campaignID = db.Column(db.Integer,primary_key = True,autoincrement = True)
    sponsorname = db.Column(db.String,nullable = False) 
    campaignname = db.Column(db.String,nullable = False,unique = True) 
    companyname = db.Column(db.String,nullable = False)
    budget = db.Column(db.Integer,nullable = False)
    startdate = db.Column(db.Date,nullable=False,server_default=db.text('CURRENT_DATE'))
    niche = db.Column(db.String)

class CampaignRequests(db.Model):
    __tablename__ = 'requests'
    requestID = db.Column(db.Integer,primary_key = True,autoincrement = True)
    campaignname = db.Column(db.String,nullable=False)
    influencername = db.Column(db.String)
    sponsorname = db.Column(db.String) 
    name = db.Column(db.String) 
    payment = db.Column(db.Integer)
    addetails = db.Column(db.String)
    companyname = db.Column(db.String)
    reqtype = db.Column(db.String) 
    startdate = db.Column(db.Date,nullable=False,server_default=db.text('CURRENT_DATE'))
    days = db.Column(db.Integer)

class Queries(db.Model):
    __tablename__ = 'queries'
    queryid = db.Column(db.Integer,primary_key = True,autoincrement = True)
    name = db.Column(db.String)
    query1 = db.Column(db.String)
    emailid = db.Column(db.String)  