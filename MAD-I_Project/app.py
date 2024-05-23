from flask import Flask, redirect, render_template, request 
from flask import session
from table import *
import jinja2

## done ## 
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
        #loggedin.html banao basic sa easy hi hoga 
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

## till here ## 
#done sign up login , just add siggnedin.html in this 

## to do ##
#add dashbord for different kinds kaafi time taking hoga 
@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        #save krdo info 
        name = request.form['name']
        query = request.form['query']
        email = request.form['email']
        #using js check if they given things are ok or not 
        #if ok then add it to this database 
    return render_template('contact.html')
    #contact krke admin se baat kr skte hain 

@app.route('/dashbord')
def dashbord():
    if 'type' not in session:
        return redirect('/')
    if session['type']=='admin':
        #jo bhi hain datbase mai limit 10 krke daldo as latest bolke 
        return render_template('/admindash')
        #admindash mai mai queries dikha sakta hu 
    elif session['type']=='influencer':
        #sare Waiting mai jo bhi hai , har ek ko waie decline kr skte hain 
        return redirect('/infludash')
    else:
        return render_template('/sponsordash')
    
@app.route('/infludash')
def infludash():
    if session['type']!='influencer':
        return redirect('/dashbord')
    L = CampaignRequests.query.filter_by(name=session['userid'],reqtype='W').all()
    #abhi sare div ke aage ek button dalna hain accept aur reject krne ka ya fir price change krne ka
    # req type can be Waiting,Accepted,Rejected
    return render_template('infludash.html',waitinglist=L)

if __name__ == '__main__':
    app.run(debug=True)
