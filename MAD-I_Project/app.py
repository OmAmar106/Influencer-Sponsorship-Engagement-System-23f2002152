from flask import Flask, redirect, render_template, request 
from flask import session
from table import *
import jinja2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
db.init_app(app)
app.app_context().push()
app.secret_key = "APtlnuRu04uv"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #good for performance 
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
        ####
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
            newinfluencer = Influencer(username=session['tempuname'],password=session['temppass'],name=name,category=category,reach=reach)
            db.session.add(newinfluencer)
        db.session.commit()
        session.pop('temptype',None)
        session.pop('tempuname',None)
        session.pop('temppass',None)
        return redirect('/login')
    else:
        if 'temptype' not in session:
            return redirect('/signup')
        return render_template('enterdetails.html',type=session['temptype'])

@app.route('/logout')
def logout():
    session.pop('userid',None)
    session.pop('password',None)
    session.pop('type',None)
    return redirect('/')

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        name = request.form['name']
        query = request.form['query']
        email = request.form['email']
    ####
    return render_template('contact.html')

@app.route('/dashbord')
def dashbord():
    if 'type' not in session:
        return redirect('/')
    if session['type']=='admin':
        return render_template('/admindash')
    elif session['type']=='influencer':
        return redirect('/infludash')
    else:
        return render_template('/sponsordash')
    
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
    
@app.route('/profile')
def selfprofile():
    if 'userid' not in session or session['userid']=="admin":
        return redirect('/dashbord')
    else:
        s = '/profile/'+session['userid']
        return redirect(s)
    
@app.route('/profile/<string:s>')
def profile(s):
    L = Sponsors.query.filter_by(username=s).all()
    L1 = Influencer.query.filter_by(username=s).all()
    if len(L1)==1:
        L2 = CampaignRequests.query.filter_by(influencername=s).all()
        L = Influencer.query.filter_by(username=s).all()
        L = L[0]
        return render_template('influprofile.html',waitinglist=L2,L=L)
    else:
        L2 = CampaignRequests.query.filter_by(sponsorname=s).all()
        L3 = Campaign.query.filter_by(sponsorname=s).all()
        L = Sponsors.query.filter_by(username=s).all()
        L = L[0]
        return render_template('sponsorprofile.html',waitinglist=L2,L=L,L3=L3)
if __name__ == '__main__':
    app.run(debug=True)

#kal search user wala page banana, give campaign wala option dono ke pas rakhna par agar influencer dabayega toh dashbord
#ending main comments dalna hain explaining each step to make it more understandable 
#dashbord for influencer 
#dashbord for admin - should contain query as well - and all the accepted rejected and cancel requests
#signed in page 
#search users 
#browse campaigns 
#create campaigns 
#in admin add option flag a campaign after searching it , ya toh ek search ka common page banao , with flag var for admin
#contact.html banana hain 
#search main flagged wale mat dikhao , profile mai toh kr diya alrdy 
#search influencers ke bad , use dropdown menu se tum vo de skte ho jo campaigns flagged nahi hain -> assign krne ke liye