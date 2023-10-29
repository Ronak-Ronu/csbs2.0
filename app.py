from flask import Flask,render_template,request,redirect,url_for,send_file,send_from_directory
from flask_sqlalchemy import SQLAlchemy
import flask
from flask_mail import Mail,Message
from config import mail_username,mail_password
from datetime import datetime
from whatsappmsg import get_text_message_input, send_message,get_image_message_input
import json
import asyncio
from waresources import resources
from flask_caching import Cache
import numpy as np
import matplotlib.pyplot as plt
import requests
import time
# from flask_frozen import Freezer

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
app=Flask(__name__)
cache.init_app(app)
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
@cache.cached(timeout=50)
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

@app.route('/MailCourse',methods=['POST','GET'])
def mailcourse():
	if request.method=='POST':
		id = int(request.form.get("id"))
		email=request.form['email']
		res=resources()
		cres= next(filter(lambda f: f['id'] == id, res), None)
		print(email)
		print(id)
		body1="""
            <html>
            <head>
                <style>
                    /* Add your CSS styling here */
                </style>
            </head>
            <body>
                <p><strong>Congratulations for getting started with helpcode404!</strong></p>
                <p><em>Visit:</em> <a href="https://github.com/Ronak-Ronu?tab=repositories">GitHub Repositories</a></p>
                <p><em>Open Document:</em> <a href="{}">{}</a></p>
				<img src="{}" width="250px" height="300px"/>
                <p><em>Topic:</em> {}</p>
                <p><em>Rating:</em> {}</p>
                <p><em>SendTo:</em> {}</p>
            </body>
            </html>
        """.format(cres["document"], cres["document"],cres["thumbnail"], cres["topic"], cres["Rating"], email)
		body = (
            f'```Congratulation for getting started. This is``` *helpcode404*.\n'
			f'*VISIT*\n {cres["thumbnail"]}\n\n'
            f'*VISIT*\n https://github.com/Ronak-Ronu?tab=repositories\n\n'
            f'*OPEN DOCUMENT* {cres["document"]}.\n'
            f'*Topic* : {cres["topic"]}\n'
            f'*Rating*:{cres["Rating"]}\n'
            f'*SendTo*:{email}'
        )
		message=Message("CODEhELP404",sender="csbs2project@gmail.com",recipients=[email])
		message.html = body1
		print(message)
		mail.send(message)
		return redirect('/helpcode404')
	return render_template('whatsapp.html')


@app.route('/Files')
def file():
	return render_template('files.html')
@app.route('/code')
def code():
	return render_template('code.html')


@app.route('/selection_sort',methods=['POST'])
def selection_sort():
	num=int(request.form['usernum'])
	lst = np.random.randint(0,100,num)
	x=np.arange(0,num,1)
	# print(num)
	input_list=lst
	print(input_list)
	for idx in range(len(input_list)):
		min_idx = idx
		for j in range( idx +1, len(input_list)):
			plt.bar(x,input_list,color='skyblue',edgecolor='#0077BE')
			plt.pause(0.001)
			plt.clf()
			plt.savefig(f'static/assets/img/frame_{j}.png')
			if input_list[min_idx] > input_list[j]:
				min_idx = j
		input_list[idx], input_list[min_idx] = input_list[min_idx], input_list[idx]
	plt.bar(x, input_list, color='skyblue', edgecolor='#0077BE')
	plt.clf() 
	time.sleep(1)
	plt.close()
	return render_template('algovisual.html')

@app.route('/bubble_sort',methods=['POST'])
def bubble_sort():
	num=int(request.form['usernum'])
	lst = np.random.randint(0,100,num)
	x=np.arange(0,num,1)
	# print(num)
	n = len(lst)

	collection=lst
	print(collection)
	for i in range(n - 1):
		swapped = False
		for j in range(n - 1 - i):
			plt.bar(x,collection,color='skyblue',edgecolor='#0077BE')
			plt.pause(0.001)
			plt.clf()
			if collection[j] > collection[j + 1]:
				swapped = True
				collection[j], collection[j + 1] = collection[j + 1], collection[j]
		if not swapped:
			break 
	plt.bar(x, collection, color='skyblue', edgecolor='#0077BE')
	plt.savefig('static/assets/img/plot.png')
	time.sleep(1)
	plt.clf() 
	plt.close()
	return render_template('algovisual.html')

@app.route('/insertion_sort',methods=['POST'])
def insertion_sort():
	num=int(request.form['usernum'])
	lst = np.random.randint(0,100,num)
	x=np.arange(0,num,1)
	# print(num)
	n = len(lst)
	InputList=lst
	for i in range(1, len(InputList)):
		j = i-1
		nxt_element = InputList[i]
		while (InputList[j] > nxt_element) and (j >= 0):
			plt.bar(x,InputList,color='skyblue',edgecolor='#0077BE')
			plt.pause(0.001)
			plt.clf()
			InputList[j+1] = InputList[j]
			j=j-1
		InputList[j+1] = nxt_element
	plt.bar(x, InputList, color='skyblue', edgecolor='#0077BE')
	plt.savefig('static/assets/img/plot.png')
	plt.clf() 
	time.sleep(1)
	plt.close()
	return render_template('algovisual.html')

def partition(arr, low, high,x):
    i = (low-1)
    pivot = arr[high]
    for j in range(low, high):
            plt.bar(x,arr,color='skyblue', edgecolor='#0077BE')
            plt.pause(0.01)
            plt.clf()
            if arr[j] <= pivot:
                i = i+1
                arr[i], arr[j] = arr[j], arr[i]

    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)

def quickSort(arr, low, high,x):
	if len(arr) == 1:
		return arr
	if low < high:
		pi = partition(arr, low, high,x)
		quickSort(arr, low, pi-1,x)
		quickSort(arr, pi+1, high,x)


@app.route('/quick_sort',methods=['POST'])
def quick_sort():
	num=int(request.form['usernum'])
	lst = np.random.randint(0,100,num)
	x=np.arange(0,num,1)
	# print(num)
	n = len(lst)
	arr=lst
	low=0
	high=n-1
	quickSort(arr, low, high,x)
	plt.bar(x, arr, color='skyblue', edgecolor='#0077BE')
	plt.savefig('static/assets/img/plot.png')
	plt.clf() 
	time.sleep(1)
	plt.close()
	return render_template('algovisual.html')


@app.route('/plot')
def plot():
    return 	send_from_directory('static/assets/img', 'plot.png')


@app.route('/visualize-code',methods=['POST','GET'])
def visualalgo():
	if request.method=='POST':
		num=request.form['usernum']
		algotype=request.form['algotype']
		print(num)
		print(algotype)
		if(  algotype.lower() =="selection"):
			requests.post('http://127.0.0.1:5000/selection_sort', data={'usernum': num})
		elif(algotype.lower()=="bubble"):
			requests.post('https://csbs20.onrender.com/bubble_sort', data={'usernum': num})
		elif(algotype.lower()=="insertion"):
			requests.post('https://csbs20.onrender.com/insertion_sort', data={'usernum': num})
		elif(algotype.lower()=="quick_sort"):
			requests.post('https://csbs20.onrender.com/quick_sort', data={'usernum': num})
	return render_template('algovisual.html')




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
   f'```Congratulation for getting started.this is``` *helpcode404*.\n*_VISIT_* \n https://github.com/Ronak-Ronu?tab=repositories \n\n *OPEN DOCUMENT* {cres["document"]}.\n*Topic* : {cres["topic"]} \n*Rating*:{cres["Rating"]} \n *SendTo*:{phno}');
   data2=get_image_message_input(app.config['RECIPIENT_WAID'],cres['thumbnail'])
   print(data1)
   await send_message(data2)
   await send_message(data1)
   return flask.redirect(flask.url_for('BLOG'))



if __name__=='__main__':
	# freezer.freeze()
	app.run(debug=True)
