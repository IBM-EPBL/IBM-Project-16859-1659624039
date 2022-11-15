from flask import Flask, render_template, request, redirect,url_for,session
import ibm_db
import re

app=Flask(__name__)

app.secret_key='a'




hostname="98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud"
uid="kzw61061"
pwd="8ktYpfXGlIuP5Pp8"
driver="{IBM DB2 ODBC DRIVER}"
db="bludb"
port=" 30875"
protocol="TCPIP"
certificate="crt.crt"

dsn=(
    " DATABASE={0};"
    " HOSTNAME={1};"
    "PORT={2};"
    "UID={3};"
    "SECURITY=SSL;"
    "SSLServerCertificate={4};"
    "PWD={5};").format(db,hostname,port,uid,certificate,pwd)
print(dsn)
try:
    conn = ibm_db.connect(dsn, '', '')
    print("Connected to db")
except:
    print("unable ")



@app.route('/')

def home():
    return  render_template('home.html')

    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg=''

    if request.method == 'POST':
        usename=request.form['username'] #form in html
        password=request.form['password']
        sql="SELECT * FROM userd WHERE username =? AND password=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,usename)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin']=True
            session['id']=account['USERNAME']
            userid=account['USERNAME']
            session['USERNAME'] = account['USERNAME']
            msg='logged in successfully !'

            msg='logge in successfully !'
            return render_template("dashboard.html",msg =msg)
        else:
            msg= 'Incorrect username/ password !'
            return render_template('login.html',msg=msg)
    return render_template('login.html')
@app.route('/register',methods =['GET','POST'])
def register():
    msg=''
    if request.method =='POST':
        usename = request.form['username']  # form in html
        email = request.form['email']
        password = request.form['password']
        name=request.form['name']
        city=request.form['city']
        gender=request.form['gender']
        phone=request.form['phone']
        blood=request.form['blood']
        report=request.form['report']

        sql = "SELECT * FROM userd WHERE username =? "
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, usename)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg='Account already exist !'
            return render_template("login.html", msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg='Invalid emmail address'
        elif not re.match(r'[A-Za-z0-9]+',usename):
            msg='name must contain character and num only'

        else:
            insert_sql ="INSERT INTO userd VALUES(?,?,?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,usename)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.bind_param(prep_stmt, 4, name)
            ibm_db.bind_param(prep_stmt, 5, city)
            ibm_db.bind_param(prep_stmt, 6, gender)
            ibm_db.bind_param(prep_stmt, 7, phone)
            ibm_db.bind_param(prep_stmt, 8, blood)
            ibm_db.bind_param(prep_stmt, 9, report)



            ibm_db.execute(prep_stmt)
            msg='you have successfully registered !'
            return render_template("dashboard.html", msg=msg)

    elif request.method =='post':
        msg ='please fill out details'
    msg = 'you have successfully registered !'
    return render_template('register.html')



@app.route('/dashboard')
def dash():

    return  render_template('dashboard.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/req',methods = ['GET','POST'])
def req():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']  # form in html
        email = request.form['email']
        address= request.form['address']
        age = request.form['age']
        city = request.form['city']
        phone = request.form['phone']
        blood = request.form['blood']
        insert_sql = "INSERT INTO requser VALUES(?,?,?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, name)
        ibm_db.bind_param(prep_stmt, 2, email)
        ibm_db.bind_param(prep_stmt, 3, address)
        ibm_db.bind_param(prep_stmt, 4, age)
        ibm_db.bind_param(prep_stmt, 5, city)
        ibm_db.bind_param(prep_stmt, 6, phone)
        ibm_db.bind_param(prep_stmt, 7, blood)
        ibm_db.execute(prep_stmt)
        msg = 'you have successfully registered !'
        return render_template("home.html", msg=msg)
    else:
        msg ='please fill out details'
    return render_template('req.html')

@app.route('/contactus' ,methods = ['GET','POST'])
def contactus():
    return render_template('contactus.html')

@app.route('/aboutus' ,methods = ['GET','POST'])
def aboutus():
    return render_template('aboutus.html')

@app.route('/apply',methods = ['GET','POST'])

def apply():
    msg=''
    if request.method =='POST':
        usename = request.form['username']  # form in html
        email = request.form['email']

        qualification =request.form['qualification']
        skills =request.form['skills']
        jobs = request.form['s']
        sql = "SELECT * FORM users WHERE username =?"

        insert_sql ="INSERT INTO job values(?,?,?,?,?)"
        prep_stmt =ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt, 1, usename)
        ibm_db.bind_param(prep_stmt, 2, email)
        ibm_db.bind_param(prep_stmt, 3, qualification)
        ibm_db.bind_param(prep_stmt, 4, skills)
        ibm_db.bind_param(prep_stmt,5,jobs)
        ibm_db.execute(prep_stmt)
        msg='You have successfully applied for job !'

    elif request.method =='POST':
        msg='Please fill out the form !'

    return render_template('apply.html' ,msg=msg)

@app.route('/display')
def display():
    print(session["username"],session['id'])

    cursor =mysql.connection.cursor()
    cursor.execute('SELECT &FROM  job WHERE userid =%s',(session['id'],))
    account = cursor.fetchone()
    print("account display,account")

    return render_template('display.html',account=account)

@app.route('/logout')

def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return render_template('home.html')


if __name__=="__main__":
    app.debug=True
    app.run(host = '0.0.0.0',port=5000)











