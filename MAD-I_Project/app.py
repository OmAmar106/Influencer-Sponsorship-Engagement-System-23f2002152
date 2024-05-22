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

#abhi ye krna hai 
@app.route('/login',methods=['GET','POST'])
def login():
    if 'userid' not in session:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            #first check if the username and password are correct or not 
            if username=='admin' and password=='#pas123':
                session['userid'] = username
                session['password'] = password
                session['type'] = 'admin'
                return redirect('/dashbord')
            else:
                #check karo if true
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
                #agar sponsor hain toh sponsordashbord karo warna fir influencer dashbord 
                #agar exist nahi krta tohi krna hain 
            return render_template('login.html',flag=True)
        else:
            return render_template('login.html')
    else:
        #return the fact that user has already logged in 
        return render_template('loggedin.html',name=session['userid'])

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name = request.form['username']
        password = request.form['password']
        #ab check karo ki if vo already table mai hi ki nahi, nahi hain toh daalo 
        ## abhi kal idhar update krna hain ##
        ## ## 
        ## ##   
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
            #add userna me password and type
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
        #add to database
        #session pop bhi krna hain 
        db.session.commit()
        session.pop('temptype',None)
        session.pop('tempuname',None)
        session.pop('temppass',None)
        return redirect('/login')
    else:
        if 'temptype' not in session:
            return redirect('/signup')
        return render_template('enterdetails.html',type=session['temptype'])
#sign up mai usernmae cannot be that from sponsor or influencer or admin 
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
#and agar loggined nahi hain and then dashbord pe jane ki koshish kar rahe ho toh redirect to index 
@app.route('/logout')
def logout():
    session.pop('userid',None)
    session.pop('password',None)
    session.pop('type',None)
    return redirect('/')

@app.route('/dashbord')
def dashbord():
    if 'type' not in session:
        return redirect('/')
    if session['type']=='admin':
        return render_template('admindash.html')
    elif session['type']=='influencer':
        return render_template('infludash.html')
    else:
        return render_template('sponsordash.html')
    

if __name__ == '__main__':
    app.run(debug=True)
