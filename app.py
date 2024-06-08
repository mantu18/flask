from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail
import json


with open('config.json','r') as c:
    params=json.load(c)["params"]
app=Flask(__name__)
local_server=True
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db=SQLAlchemy(app)
# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT='465',
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME=params['gmail-user'],
#     MAIL_PASSWORD=params['gmail-password']
# )
# mail=Mail(app)

class Contact(db.Model):
    idcontact= db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    phone_num = db.Column(db.String(12),nullable=False)
    message = db.Column(db.String(120), nullable=False)


@app.route("/")
def home():
    posts=Posts.query.filter_by().all()
    return render_template("index.html",params=params,posts=posts)
@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        entry=Contact(Name=name,email=email,phone_num=phone,message=message)
        db.session.add(entry)
        db.session.commit()
        # mail.send_message("new message from " + name,
        #                   sender=email,
        #                   recipients=[params['gmail-user']],
        #                   body=message + "/n" +phone)

    return render_template("contact.html",params=params)
@app.route("/about") 
def about():
    return render_template("about.html",params=params)  
class Posts(db.Model):
    slno= db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(80),nullable=False)
    content = db.Column(db.String(120),nullable=False)
    date = db.Column(db.String(20),nullable=False)
    slug = db.Column(db.String(12), nullable=False)

@app.route("/post/<string:post_slug>",methods=['GET']) 
def post_fun(post_slug):
    posts=Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html",params=params,posts=posts)
app.run(debug=True)