from flask import Flask, redirect, render_template, request 
from flask import session
from table import *

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
    if 'user' not in session:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            #first check if the username and password are correct or not 
            session['userid'] = username
            session['password'] = password
            #agar exist nahi krta tohi krna hain 
            return render_template('dashbord.html')
        else:
            return render_template('login.html')
    else:
        #return the fact that user has already logged in 
        return render_template('loggedin.html')

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
if __name__ == '__main__':
    app.run(debug=True)
