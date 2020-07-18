from flask import Flask, render_template , url_for, flash, redirect
from forms import Registrationform, loginform
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

app.config['SECRET_KEY']='1cb81085f3241bfa'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@localhost:5432/WMS'

db= SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(400), nullable=False, default="No Address")
    mobno = db.Column(db.Integer,unique=True,default="0000")
    Complain= db.relationship('Complain',backref='author',lazy=True)
    

    def __init__ (self,username,email,image_file,address,mobno,password):
        self.name=username
        self.email=email
        self.image_file=image_file
        self.address=address
        self.mobno=mobno
        self.password=password

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}','{self.address}','{self.mobno}','{self.password}')"

class Complain(db.Model):
    __tablename__ = 'Complain'
    id = db.Column(db.Integer, primary_key=True)
    userid= db.Column(db.Integer,db.ForeignKey('User.id'), nullable=False)
    mob_no=db.Column(db.Integer,nullable=False)
    landmark=db.Column(db.String(200),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    tycomp=db.Column(db.String(20),nullable=False) #type of complain
    Complaint=db.Column(db.String(200),nullable=False)
    photo=db.Column(db.String(20), nullable=False, default="default2.jpg")
    dateposted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    


    def __init__(self,userid,mob_no,landmark,pincode,Complaint,photo,dateposted,tycomp):
        self.userid=userid
        self.mob_no=mob_no
        self.landmark=landmark
        self.pincode=pincode
        self.Complaint=Complaint
        self.photo=photo
        self.dateposted=dateposted
        self.tycomp=tycomp

    def __repr__(self):
        return f"Complain('{ self.userid}','{self.mob_no}','{self.landmark}','{self.pincode}','{self.Complaint}','{self.photo}','{self.dateposted}','{self.tycomp}'')"    



class admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")

    def __init__ (self,username,image_file,password):
        self.name=username
        self.image_file=image_file
        self.password=password

    def __repr__(self):
        return f"admin('{self.name}','{self.image_file}','{self.password}')"



class Solved(db.Model):
    __tablename__ = 'Solved'
    id = db.Column(db.Integer, primary_key=True)
    userid= db.Column(db.Integer,db.ForeignKey('Users.id'), nullable=False)
    mob_no=db.Column(db.Integer,nullable=False)
    landmark=db.Column(db.String(200),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    tycomp=db.Column(db.String(20),nullable=False) #type of complain
    Complaint=db.Column(db.String(200),nullable=False)
    datesaw=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)



    def __init__(self,userid,mob_no,landmark,pincode,Complaint,datesaw,tycomp):
        self.userid=userid
        self.mob_no=mob_no
        self.landmark=landmark
        self.pincode=pincode
        self.Complaint=Complaint
        self.datesaw=datesaw
        self.tycomp=tycomp

    def __repr__(self):
        return f"Complain('{ self.userid}','{self.mob_no}','{self.landmark}','{self.pincode}','{self.Complaint}','{self.datesaw}','{self.tycomp}'')"    



    







    
    


@app.route('/')
@app.route("/home")
def home():
    return  render_template("home.html")

@app.route("/about")
def about():
    return  render_template("about.html", title='ABOUT')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = loginform()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/reg", methods=['GET','POST'])
def reg():
    form = Registrationform()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return  render_template("reg.html", title='REGISTER',form=form)

if __name__=="__main__":
    app.run(debug=True)    