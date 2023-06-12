from flask import Flask,render_template,request,redirect,url_for,send_file
from flask_sqlalchemy import SQLAlchemy
import flask
from flask_mail import Mail,Message
from config import mail_username,mail_password
from datetime import datetime
from whatsappmsg import get_text_message_input, send_message,get_templated_message_input
import json
import asyncio
from waresources import resources
# from flask_frozen import Freezer

app=Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']=mail_username
app.config['MAIL_PASSWORD']=mail_password
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///userdata.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

mail = Mail(app)

class user(db.Model):
	sno=db.Column(db.Integer,primary_key=True)
	pswd=db.Column(db.String(199),nullable=False)
	name=db.Column(db.String(150),unique=True,nullable=False)
	birthday=db.Column(db.String(100),nullable=False)
	time_joined=db.Column(db.DateTime,default=datetime.utcnow)
	#def __repr__(self)->str:
	#	return f"{self.sno} - {self.name} - {self.birthday} - {self.pswd}"
class Comment(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	text=db.Column(db.String(200),nullable=False)
	date_commented=db.Column(db.DateTime(timezone=True),default=datetime.utcnow)

with open('config.json') as f:
    config = json.load(f)
app.config.update(config)

@app.route('/')
def home():
	return render_template('HOMEPAGE.html')

@app.route('/gotoclass')
def go_class():
	userdata=user.query.all()
	return render_template('goto_class.html',userdata=userdata)

@app.route('/addme')
def ADDME():
	return render_template('add_me.html')

@app.route('/rate')
def rate():
	return render_template('rate.html')


@app.route('/blog')
def BLOG():
	return render_template('index.html')


@app.route('/data',methods=['POST','GET'])
def showdata():
	if request.method=='POST':
		uname=request.form['username']
		upass=request.form['upassword']
		dob=request.form['bday']
		# file=request.files['file']
		User=user(name=uname,birthday=dob,pswd=upass)
		db.session.add(User)
		db.session.commit()
	# data = request.form.get('add_me.html')
	userdata=user.query.all()
	if(uname=='ronu' and upass=="1234"):
		return render_template('table.html',userdata=userdata)
	return render_template('requested.html')

@app.route('/adduser')
def adduser():
		userdata=user.query.all()
		return render_template('goto_class.html',userdata=userdata)

@app.route('/create-comment',methods=['POST','GET'])
def create_comment():
	text=request.form.get('Txt')
	if not text:
		flash("cannot post empty ctextAreaExampleomment.",category='error')
	else:
		comment=Comment(text=text)
		db.session.add(comment)
		db.session.commit()
		data=Comment.query.all()
	return render_template('post2.html',data=data)

@app.route('/post')
def post():
	return render_template('post.html')
@app.route('/post1')
def post1():
	return render_template('post1.html')
@app.route('/post2',methods=['POST','GET'])
def post2():
	return render_template('post2.html')
@app.route('/post3')
def post3():
	return render_template('post3.html') 
@app.route('/downloads/book1')
def tos():
    # workingdir = os.path.abspath(os.getcwd())
    filepath = 'static/files/book1.pdf'
    return send_file(filepath, as_attachment=True)
@app.route('/downloads/book2')
def tos1():
    # workingdir = os.path.abspath(os.getcwd())
    filepath = 'static/files/book2.pdf'
    return send_file(filepath, as_attachment=True)


@app.route('/email-contact',methods=['POST','GET'])
def emailcnt():
	if request.method=='POST':
		name=request.form['NAME']
		email=request.form['EMAIL']
		sub=request.form['SUBJECT'] 
		msg=request.form['MESSAGE']
		print(name)
		message=Message(sub,sender=email,recipients=[mail_username])
		message.body = f"MESSAGE : \n \t {msg}\n\n Name : {name}\nEmail : {email} \n\n \t THANK YOU FOR CONNECTING : {name}"
		mail.send(message)
		return redirect('/blog')
	return render_template('contact.html')


@app.route('/Files')
def file():
	return render_template('files.html')
@app.route('/code')
def code():
	return render_template('code.html')
@app.errorhandler(404)
def error_404(e):
	return render_template('404.html'),404

@app.route('/helpcode404')
def helpcode404():
	return render_template('whatsapp.html',resource=resources())

@app.route('/whatsappform', methods=['POST'])
async def welcome():
   id = int(request.form.get("id"))
   phno=request.form.get("phoneno")
   res=resources()
   cres= next(filter(lambda f: f['id'] == id, res), None)
   data1 = get_text_message_input(app.config['RECIPIENT_WAID'],
   f'```Congratulation for getting started.this is``` *helpcode404*.\n_VISIT_ \n https://github.com/Ronak-Ronu?tab=repositories \n *OPEN* {cres["document"]}.\n*Topic* : {cres["topic"]} \n*Rating*:{cres["Rating"]} \n *SendTo*:{phno}');
   data2 = get_templated_message_input(app.config['RECIPIENT_WAID'], cres)
   print(data1)
   await send_message(data1)
   return flask.redirect(flask.url_for('BLOG'))

if __name__=='__main__':
	# freezer.freeze()
	app.run(debug=True)
