#  miniflask project/run.py
from flask import Flask,request,redirect
from flask import url_for,render_template

# Login 
from flask import session as login_session
from functools import wraps

# For Flash Messages
from flask import flash
xargs=xwraps=None
# automatically redirects login page if the user doesnt login and try to do some operations(delete,update,view)
def required_login(f):
	@wraps(f) # args takes number of arguments in tuple, wraps take data in dictionary format(email & password)
	def x(*args,**wraps):
		global xargs,xwraps
		xargs=args;xwraps=wraps
		if 'email' not in login_session:
			return redirect(url_for('login')) # url_for redirects to login page
		return f(*args,**wraps) # if already login then goes to required page.
	return x # returns output to @required_login.

from os import getcwd,remove # returns file current working directory of this file.
# remove is used to remove file.
# Import db_setup.py into this python file
from db_setup import Base,Student
# Base is used a structure object (or) table.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
engine= create_engine("sqlite:///mydb.db") # database object is created using sqlite database
Base.metadata.bind=engine # operations that should be stored in database
session=(scoped_session(sessionmaker(\
								bind=engine))) # for performing operation on data in database

app=Flask(__name__) # app object is created
@app.route("/") # create url.
@app.route("/home")
def home():
	return render_template("home.html") # open html file in browser.

#post = sending data from one file to another file without dispalying data in url.
#get = sending data from one file to another file data displayed in url.
@app.route("/register",methods=["POST","GET"])	
def register():
	# transfered html data stored in request object
	if request.method=="POST":
		# if password and re-enter password same then if condition statements executed.
		if request.form["psw"]==request.form["psw-repeat"]:
			# image file we have choosen in html file should be saved in static/images folder of our project folder path.
			file=request.files["img"]			
			path=getcwd()+"\\static\\images\\"
			file.save(path+file.filename)
			# name is variable and "name" is html element name value.
			name=request.form["name"]
			mobile=request.form["number"]
			gender=request.form["gender"]
			email=request.form["email"]
			pwd=request.form["psw"]
			picture=file.filename
			# database column name(name) = (name)variable name where html form data.
			student_info=Student(name=name,
				mobile=mobile,
				gender=gender,
				email=email,
				password=pwd,
				image=picture)
			session.add(student_info) #storing stuent info temporarly in session object.
			session.commit() # permantely storing
			flash("Successfully Inserted.","success")
			return redirect(url_for("home"))
		flash("Both passwords are not Matched","danger") # if entered passwords are mismatch then we will return none(nothing).
		return redirect(url_for('register'))
	else:
		return render_template("register.html") # if post method is not there in redirects register.html.

@app.route("/login",methods=["POST","GET"])	
def login():
	if request.method=="POST":
		email=request.form["username"]
		password=request.form["password"]
		login_info=session.query(Student).\
		filter_by(email=email,password=\
			password).one_or_none()
		if login_info!=None:
			login_session["email"]=email
			login_session["password"]=password
			flash("Welcome to Page.","success")
			return redirect(url_for('home'))
		else:
			flash("username & password\
				are not valid.","error")
	else:
		if 'email' in login_session:
			flash("You already Logined if u not login first logout current Account","error")
			return redirect(url_for("home"))
	return render_template("login.html")

# display which data entered in register.html
@app.route("/view")
@required_login
def view():
	user_info=session.query(Student).filter_by(email=login_session["email"]).one()
	return render_template("view.html",user=user_info)

@app.route("/update",methods=["POST","GET"])
@required_login
def update():
	if request.method=="POST":
		update_info=session.query(Student).filter_by(email=login_session["email"]).one()
		if len(request.files['img'].filename):
			remove(getcwd()+"\\static\\images\\"+update_info.image)
			file=request.files["img"]			
			path=getcwd()+"\\static\\images\\"
			file.save(path+file.filename)
			update_info.image=file.filename

		update_info.name = request.form["name"]
		update_info.mobile =request.form["number"]
		update_info.gender = request.form["gender"]
		update_info.password = request.form["psw"]
		session.commit()
		flash("Updated Successfully.","primary")
		return redirect(url_for('home'))
	else:
		user_info=session.query(Student).filter_by(email=login_session["email"]).one()
		return render_template("update.html",user=user_info)

# user needed to logout from account
@app.route("/logout")
@required_login
def logout():
	if len(login_session["email"]):
		del login_session["email"]
		del login_session["password"]
		return redirect(url_for('home'))

@app.route("/delete")
@required_login
def delete():
	user=login_session['email']
	delete_info=session.query(Student).filter_by(email=user).one()
	remove(getcwd()+"\\static\\images\\"+delete_info.image)
	session.delete(delete_info)
	session.commit()
	del login_session["email"]
	del login_session["password"]
	flash("Your Account is Removed Sucessfully.","success")
	return redirect(url_for('home'))

@app.route("/contact")
def contact():
	return render_template("contacts.html")

@app.route('/check')
def check():
	return str(xargs)

if __name__ == "__main__":
	app.secret_key="123456789"
	app.run(debug=True,port=5000,host="localhost")