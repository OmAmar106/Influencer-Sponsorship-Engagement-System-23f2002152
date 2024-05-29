from flask import Flask, redirect, render_template, request, jsonify
from flask import session
from table import *
import jinja2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
db.init_app(app)
app.app_context().push()
app.secret_key = "APtlnuRu04uv"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
with app.app_context():
    db.create_all()
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if 'userid' not in session:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username=='admin' and password=='#pas123':
                session['userid'] = username
                session['password'] = password
                session['type'] = 'admin'
                return redirect('/dashbord')
            else:
                sponsors = Sponsors.query.all()
                for i in sponsors:
                    if i.username==username and i.password==password:
                        session['userid'] = username
                        session['password'] = password
                        session['type'] = 'sponsor'
                        return redirect('/dashbord')
                influencers = Influencer.query.all()
                for i in influencers:
                    if i.username==username and i.password==password:
                        session['userid'] = username
                        session['password'] = password
                        session['type'] = 'influencer'
                        return redirect('/dashbord')
            return render_template('login.html',flag=True)
        else:
            return render_template('login.html')
    else:
        return render_template('loggedin.html',name=session['userid'])

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name = request.form['username']
        password = request.form['password']
        if name=='admin':
            return render_template('signup.html',flag=True)
        sponsors = Sponsors.query.all()
        flag = False
        for i in sponsors:
            if i.username==name:
                flag = True
        if flag:
            return render_template('signup.html',flag=True)
        influencers = Influencer.query.all()
        for i in influencers:
            if i.username==name:
                flag = True
        if flag:
            return render_template('signup.html',flag=True)
        else:
            session['tempuname'] = name
            session['temppass'] = password
            return redirect('/type')
    else:
        return render_template('signup.html',flag=False)

@app.route('/type',methods=['GET','POST'])
def type():
    if request.method=='POST':
        if 'tempuname' in session:
            if 'sponsor' in request.form:
                session['temptype'] = 'sponsor'
            else:
                session['temptype'] = 'influencer'
            return redirect('/details')
        else:
            return redirect('/signup')
    else:
        return render_template('choice.html')

@app.route('/details',methods=['GET','POST'])
def enterdetails():
    if request.method=='POST':
        if session['temptype']=='sponsor':
            name = request.form['name']
            industry = request.form['industrycategory']
            budget = request.form['budgetreach']
            newsponsor = Sponsors(username=session['tempuname'],password=session['temppass'],companyname=name,industry=industry,budget=budget)
            db.session.add(newsponsor)
        else:
            name = request.form['name']
            category = request.form['industrycategory']
            reach = request.form['budgetreach']
            newinfluencer = Influencer(username=session['tempuname'],password=session['temppass'],name=name,category=category,reach=reach,niche="")
            db.session.add(newinfluencer)
        db.session.commit()
        session.pop('temptype',None)
        session.pop('tempuname',None)
        session.pop('temppass',None)
        return redirect('/login')
    else:
        if 'temptype' not in session:
            return redirect('/signup')
        return render_template('enterdetails.html',type=session['temptype'],L=db.session.query(Influencer.category).distinct().all())

@app.route('/logout')
def logout():
    L = []
    for i in session:
        L.append(i)
    for i in L:
        session.pop(i,'None')
    return redirect('/')

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        name = request.form['name']
        query = request.form['query']
        emailid = request.form['emailid']
        L = Queries(name=name,query1=query,emailid=emailid)
        db.session.add(L)
        db.session.commit()
        return redirect('/dashbord')
    return render_template('contact.html')

@app.route('/dashbord')
def dashbord():
    if 'type' not in session:
        return redirect('/')
    if session['type']=='admin':
        return redirect('/admindash')
    elif session['type']=='influencer':
        return redirect('/infludash')
    else:
        return redirect('/sponsordash')
    
@app.route('/sponsordash',methods=['POST','GET'])
def sponsordash():
    if request.method=='GET':
        if session['type']!='sponsor':
            return redirect('/dashbord')
        L = CampaignRequests.query.filter_by(name=session['userid'],reqtype='W').all()
        return render_template('sponsordash.html',waitinglist=L)
    else:
        L = CampaignRequests.query.filter_by(requestID=request.form['reqID'])
        L = L[0]
        if 'accept' in request.form:
            L.reqtype = 'W'
            L.name = L.influencername
        elif 'reject' in request.form:
            L.reqtype = 'R'
        else:
            L.payment = request.form['budget']
            L.name = L.influencername
        db.session.commit()
        return redirect('/sponsordash')

@app.route('/infludash',methods=['POST','GET'])
def infludash():
    if request.method=='GET':
        if session['type']!='influencer':
            return redirect('/dashbord')
        L = CampaignRequests.query.filter_by(name=session['userid'],reqtype='W').all()
        return render_template('infludash.html',waitinglist=L)
    else:
        L = CampaignRequests.query.filter_by(requestID=request.form['reqID'])
        L = L[0]
        if 'accept' in request.form:
            L.reqtype = 'A'
        elif 'reject' in request.form:
            L.reqtype = 'R'
        else:
            L.payment = request.form['budget']
            L.name = L.sponsorname
        db.session.commit()
        return redirect('/infludash')
    
@app.route('/admindash',methods=['POST','GET'])
def admindash():
    flag = False
    if 'type' not in session or session['type']!='admin':
        return redirect('/dashbord')
    if request.method=='POST':
        name = request.form['name']
        L2 = Influencer.query.filter_by(username=name).all()
        L3 = Sponsors.query.filter_by(username=name).all()
        if L2:
            L4 = CampaignRequests.query.filter_by(influencername=name).all()
            for i in L4:
                db.session.delete(i)
            db.session.delete(L2[0])
            db.session.commit()
        elif L3:
            L4 = CampaignRequests.query.filter_by(sponsorname=name).all()
            for i in L4:
                db.session.delete(i)
            L4 = Campaign.query.filter_by(sponsorname=name).all()
            for i in L4:
                db.session.delete(i)
            db.session.delete(L3[0])
            db.session.commit()
        else:
            return redirect('/users')             
        flag = True
    L1 = Campaign.query.all()
    L = CampaignRequests.query.all()
    query = Queries.query.all()
    a = len(Influencer.query.all())
    b = len(Sponsors.query.all())
    c = len(CampaignRequests.query.filter_by(reqtype='A').all())
    d = len(CampaignRequests.query.filter_by(reqtype='R').all())
    e = len(CampaignRequests.query.filter_by(reqtype='W').all())
    f = len(L1)
    return render_template('admindashbord.html',waitinglist=L,waitinglist1=L1,flag=flag,query=query,a=a,b=b,c=c,d=d,e=e,f=f)

@app.route('/profile')
def selfprofile():
    if 'userid' not in session or session['userid']=="admin":
        return redirect('/dashbord')
    else:
        s = '/profile/'+session['userid']
        return redirect(s)
    
@app.route('/profile/<string:s>',methods=['POST','GET'])
def profile(s):
    if request.method=='POST':
        if 'reach' in request.form:
            reach = request.form['reach']
            category = request.form['category']
            niche = request.form['niche']
            L = Influencer.query.filter_by(username=s).all()
            L = L[0]
            L.reach = reach
            L.category = category
            L.niche = niche
            db.session.commit()
            return redirect('/profile')
        flag1 = False
        flag2 = False
        for i in request.form:
            if 'modify' in i:
                flag1 = True
                break
            elif 'delete1' in i:
                flag2 = True
                break
        if flag1:
            session['modify'] = request.form['modify']
            return redirect('/create')
        elif flag2:
            campaignid = request.form['delete1']
            L = Campaign.query.filter_by(campaignID = campaignid).all()
            L = L[0]
            st = L.campaignname
            db.session.delete(L)
            L = CampaignRequests.query.filter_by(campaignname=st).all()
            for i in L:
                db.session.delete(i)
            db.session.commit()
        else:
            requestID = request.form['delete']
            L = CampaignRequests.query.filter_by(requestID=requestID).all()
            L = L[0]
            db.session.delete(L)
            db.session.commit()
        L2 = CampaignRequests.query.filter_by(sponsorname=s).all()
        L3 = Campaign.query.filter_by(sponsorname=s).all()
        L = Sponsors.query.filter_by(username=s).all()
        L = L[0]
        flag = False
        if 'userid' in session and (session['userid']==s or session['userid']=='admin'):
            flag = True
        string = ''
        if 'userid' in session and session['userid']==s:
            string = 'Delete'
        else:
            string = 'Flag'
        return redirect('/profile/'+s)
    L = Sponsors.query.filter_by(username=s).all()
    L1 = Influencer.query.filter_by(username=s).all()
    if len(L1)==1:
        flag = False
        if 'userid' in session and session['userid']==s:
            flag = True
        L2 = CampaignRequests.query.filter_by(influencername=s).all()
        L = Influencer.query.filter_by(username=s).all()
        L = L[0]
        return render_template('influprofile.html',waitinglist=L2,L=L,flag=flag)
    elif len(L)==1:
        L2 = CampaignRequests.query.filter_by(sponsorname=s).all()
        L3 = Campaign.query.filter_by(sponsorname=s).all()
        L = Sponsors.query.filter_by(username=s).all()
        L = L[0]
        flag = False
        if 'userid' in session and (session['userid']==s or session['userid']=='admin'):
            flag = True
        string = ''
        if 'userid' in session and session['userid']==s:
            string = 'Delete'
        elif 'userid' in session and session['userid']=='admin':
            string = 'Flag'
        return render_template('sponsorprofile.html',waitinglist=L2,L=L,L3=L3,flag=flag,string=string)
    else:
        return redirect('/dashbord')
    
@app.route('/users',methods=['POST','GET'])
def searchusers():
    if request.method=='GET':
        L = Influencer.query.all()
        L1 = Sponsors.query.all()
        category = db.session.query(Influencer.category).distinct().all()
        return render_template('users.html',influencer=L,sponsor=L1,st='',category=category)
    else:
        st = request.form['name']
        if request.form['type']=='influencer':
            if request.form['followers']=='':
                follow = 0
            else:
                follow = request.form['followers']
            if request.form['category']=="":
                L = Influencer.query.filter(Influencer.reach>=follow).all()
            else:
                L = Influencer.query.filter(Influencer.reach>=follow,Influencer.category==request.form['category']).all()
            L1 = []
        elif request.form['type']=='sponsor':
            if request.form['budget']=='':
                budget = 0
            else:
                budget = request.form['budget']
            L1 = Sponsors.query.filter(Sponsors.budget>=budget).all()
            L = []
        else:
            L = Influencer.query.all()
            L1 = Sponsors.query.all()
        category = db.session.query(Influencer.category).distinct().all()
        return render_template('users.html',influencer=L,sponsor=L1,st=st,category=category)
    
@app.route('/create',methods=['POST','GET'])
def createcamp():
    if request.method=='GET':
        if 'type' in session and session['type']=='sponsor':
            if 'modify' in session:
                L = Campaign.query.filter_by(campaignID=int(session['modify']),sponsorname=session['userid']).all()
                if len(L)!=0:
                    L = L[0]
                else:
                    L = Campaign(campaignname="",budget=0)
                return render_template('create.html',L=L,niche=db.session.query(Campaign.niche).distinct().all())
            else:
                return render_template('create.html',L = Campaign(campaignname="",budget=0),niche=db.session.query(Campaign.niche).distinct().all())
        else:
            return redirect('/dashbord')
    else:
        if 'type' in session and session['type']=='sponsor' and 'modify' in session:
            campaignname = request.form['campaignname']
            budget = request.form['budget']
            niche = request.form['niche']
            company = Sponsors.query.filter_by(username=session['userid']).all()
            company = company[0].companyname
            L = Campaign.query.filter_by(campaignID=session['modify']).all()
            L = L[0]
            L1 = Campaign.query.filter_by(campaignname=campaignname).all()
            for i in L1:
                if i.campaignID!=int(session['modify']):
                    return render_template('create.html',flag=True,L=L,niche=db.session.query(Campaign.niche).distinct().all())
            L1 = CampaignRequests.query.all()
            for i in L1:
                if i.campaignname==L.campaignname:
                    i.campaignname = campaignname
                    i.budget = budget
                    i.niche = niche
            db.session.delete(L)
            db.session.commit()
            session.pop('modify',None)
            L = Campaign(sponsorname=session['userid'],campaignname=campaignname,budget=budget,companyname=company,niche=niche)
            db.session.add(L)
            db.session.commit()
            return redirect('/profile')
        elif 'type' in session and session['type']=='sponsor':
            campaignname = request.form['campaignname']
            niche = request.form['niche']
            L1 = Campaign.query.filter_by(campaignname=campaignname).all()
            if L1:
                return render_template('create.html',flag=True,L= Campaign(campaignname="",budget=0),niche=db.session.query(Campaign.niche).distinct().all())
            budget = request.form['budget']
            company = Sponsors.query.filter_by(username=session['userid']).all()
            company = company[0].companyname
            L = Campaign(sponsorname=session['userid'],campaignname=campaignname,budget=budget,companyname=company,niche=niche)
            db.session.add(L)
            db.session.commit()
            return redirect('/profile')
        else:
            return redirect('/dashbord')
        
@app.route('/campaigns',methods=['POST','GET'])
def bcampaigns():
    if request.method=='GET':
        flag = False
        flag1 = False
        if 'type' in session and session['type']=='sponsor':
            flag = True
        elif 'type' in session and session['type']=='influencer':
            flag1 = True
        L3 = Campaign.query.all()
        return render_template('campaign.html',flag=flag,L3=L3,st='',flag1=flag1,niche=db.session.query(Campaign.niche).distinct().all())
    else:
        flag = False
        flag1 = False
        st = request.form['name']
        budget = request.form['budget']
        niche = request.form['niche']
        if 'type' in session and session['type']=='sponsor':
            flag = True
        elif 'type' in session and session['type']=='influencer':
            flag1 = True
        print(niche)
        if niche=="":
            L3 = Campaign.query.filter(Campaign.budget>=budget).all()
        else:
            L3 = Campaign.query.filter(Campaign.budget>=budget,Campaign.niche==niche).all()
        return render_template('campaign.html',flag=flag,L3=L3,st=st,flag1=flag1,niche=db.session.query(Campaign.niche).distinct().all())
    
@app.route('/ad/<int:n>',methods=['POST','GET'])
def requestad(n):
    if 'type' not in session or session['type']!='influencer':
        return redirect('/dashbord')
    if request.method=='GET':
        L = Campaign.query.filter_by(campaignID=n).all()
        if L:
            pass
        else:
            return redirect('/profile')
        return render_template('requestad.html',L=L[0])
    else:
        L = Campaign.query.filter_by(campaignID=n).all()
        L = L[0]
        payment = request.form['budget']
        addetails = request.form['details']
        L1 = CampaignRequests(campaignname=L.campaignname,influencername=session['userid'],sponsorname=L.sponsorname,name=L.sponsorname,payment=payment,addetails=addetails,companyname=L.companyname,reqtype='W')
        db.session.add(L1)
        db.session.commit()
        return redirect('/profile')
    
@app.route('/ad',methods=['POST','GET'])
def createad():
    if 'type' not in session or session['type']!='sponsor':
        return redirect('/dashbord')
    if request.method=='GET':
        L = Campaign.query.all()
        if L:
            pass
        else:
            return redirect('/profile')
        return render_template('createad.html',L=L)
    else:
        campaignname = request.form['options']
        L = Campaign.query.filter_by(campaignname=campaignname).all()
        L = L[0]
        payment = request.form['budget']
        addetails = request.form['details']
        influencername = request.form['influencername']
        L1 = Influencer.query.filter_by(username=influencername).all()
        if L1:
            pass
        else:
            return redirect('/users')
        L1 = CampaignRequests(campaignname=campaignname,influencername=influencername,sponsorname=session['userid'],name=influencername,payment=payment,addetails=addetails,companyname=L.companyname,reqtype='W')
        db.session.add(L1)
        db.session.commit()
        return redirect('/profile')
    
@app.route('/api/user/<string:s>',methods=['GET'])
def apiuser(s):
    L = Influencer.query.filter_by(username=s).all()
    L1 = Sponsors.query.filter_by(username=s).all()
    if L:
        L = L[0]
        d = {
            "usertype":"influencer",
            "username":L.username,
            "name":L.name,
            "category":L.category,
            "reach":L.reach,
            "niche":L.niche
        }
        return jsonify(d)
    elif L1:
        L1 = L1[0]
        d = {
            "usertype":"sponsor",
            "username":L1.username,
            "companyname":L1.companyname,
            "industry":L1.industry,
            "budget":L1.budget
        }
        return jsonify(d)
    else:
        return jsonify({"user":s+" does not exist"}) 

@app.route('/api/campaign/<string:s>')
def apicampaign(s):
    L = Campaign.query.filter_by(campaignname=s).all()
    if L:
        L = L[0]
        d = {
            "sponsorname":L.sponsorname,
            "campaignname":L.campaignname,
            "companyname":L.companyname,
            "budget":L.budget,
            "startdate":L.startdate,
            "niche":L.niche
        }
        return jsonify(d)
    else:
        return jsonify({"name":s+" does not exists"})
    
@app.route('/api/ad/<string:s>')
def apiad(s):
    L2 = CampaignRequests.query.filter_by(campaignname=s).all()
    if L2:
        d1 = {}
        for L in L2:
            if L.reqtype=='W':
                reqtype="Pending"
            elif L.reqtype=='R':
                reqtype="Rejected"
            else:
                reqtype="Accepted"
            d = {
                "sponsorname":L.sponsorname,
                "campaignname":L.campaignname,
                "influencername":L.influencername,
                "companyname":L.companyname,
                "payment":L.payment,
                "addetails":L.addetails,
                "reqtype":reqtype
            }
            d1[L2.index(L)+1] = d
        return jsonify(d1)
    else:
        return jsonify({"name":s+" does not exists"})
    
if __name__ == '__main__':
    app.run(debug=True)
