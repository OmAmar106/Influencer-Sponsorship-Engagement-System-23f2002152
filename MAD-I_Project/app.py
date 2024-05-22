from flask import Flask, redirect, render_template, request 
from flask import session
from table import *
import jinja2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
db.init_app(app)
app.app_context().push()
app.secret_key = "APtlnuRu04uv"

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
                session['userid'] = username
                session['password'] = password
                session['type'] = 'influencer'
                #agar sponsor hain toh sponsordashbord karo warna fir influencer dashbord 
            #agar exist nahi krta tohi krna hain 
                return redirect('/dashbord')
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
        return redirect('/login')
    else:
        return render_template('signup.html',flag=False)
    
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
