from flask import Flask, render_template , url_for, flash, redirect
from forms import Registrationform, loginform
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

app.config['SECRET_KEY']='1cb81085f3241bfa'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@localhost:5432/WMS'

db= SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(400), nullable=False, default="No Address")
    mobno = db.Column(db.Integer,unique=True,default="0000")
    
    def __init__ (self,username,email,image_file,address,mobno):
        self.name=username
        self.email=email
        self.image_file=image_file
        self.address=address
        self.mobno=mobno

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}','{self.address}','{self.mobno}')"

class Complain(db.Model):
    __tablename__ = 'Complains'
     id = db.Column(db.Integer, primary_key=True)
     userid= db.Column(db.Integer,db.ForeignKey('Users.id'), nullable=False)
    
    


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