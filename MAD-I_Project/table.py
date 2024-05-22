from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()
#table containing the name of the sponsor 
class Sponsors(db.Model):
    __tablename__ = 'sponsors'
    ID = db.Column(db.Integer,primary_key = True,autoincrement = True)
    username = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    companyname = db.Column(db.String,nullable=False)
    industry = db.Column(db.String,nullable=False)
    budget = db.Column(db.Integer,nullable=False)

#table containing the name of the influencers
class Influencer(db.Model):
    __tablename__ = 'influencer'
    ID = db.Column(db.Integer,primary_key = True,autoincrement = True)
    username = db.Column(db.String,nullable = False,unique = True)
    password = db.Column(db.String,nullable = False)
    name = db.Column(db.String,nullable = False)
    category = db.Column(db.String,nullable = False)  
    reach = db.Column(db.Integer,nullable = False)

class Campaign(db.Model):
    __tablename__ = 'campaign'
    campaignID = db.Column(db.Integer,primary_key = True,autoincrement = True)
    sponsorID = db.Column(db.String,nullable = False,unique = True)
    campaignname = db.Column(db.String,nullable = False,unique = True)
    flag = db.Column(db.Integer,nullable=False) #if flagged then the campaign wont be shown anymore 

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

#add a feature in which admin can ban a person just use delete from table ... where .. 
