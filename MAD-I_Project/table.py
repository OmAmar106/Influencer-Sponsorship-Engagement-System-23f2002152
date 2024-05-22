from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()
#table containing the name of the sponsor 
class Sponsors(db.Model):
    __tablename__ = 'sponsor'
    ID = db.Column(db.Integer,primary_key = True,autoincrement = True)
    username = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False,unique = True)

#table containing the name of the influencers
class Influencer(db.Model):
    __tablename__ = 'influencer'
    ID = db.Column(db.Integer,primary_key = True,autoincrement = True)
    username = db.Column(db.String,nullable = False,unique = True)
    password = db.Column(db.String,nullable = False,unique = True)

class Campaign(db.Model):
    __tablename__ = 'campaign'
    campaignID = db.Column(db.Integer,primary_key = True,autoincrement = True)
    sponsorID = db.Column(db.String,nullable = False,unique = True)
    campaignname = db.Column(db.String,nullable = False,unique = True)

class CampaignRequests(db.Model):
    __tablename__ = 'requests'
    requestID = db.Column(db.Integer,primary_key = True,autoincrement = True)
    campaignID = db.Column(db.Integer)
    influencerID = db.Column(db.String)
    reqtype = db.Column(db.String) #of 4 types,1. influencer asked the sponsor,2. Sponsor asked the influencer
    #along with accepted yet or not accepted yet if not accepted , it should be displayed on that persons homepage 

#contact us wale page pe ye hoga 
class Queries(db.Model):
    __tablename__ = 'queries'
    queryid = db.Column(db.Integer,primary_key = True,autoincrement = True)
    name = db.Column(db.String)
    query = db.Column(db.String)
    emailid = db.Column(db.String)
