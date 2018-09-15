import hashlib
import requests
from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def hashPassword(password):
    return hashlib.sha224(password.encode('utf-8')).hexdigest()

def isValid(text):
    if(len(text)>6 and any(x.isdigit() for x in text) and any(x.isupper() for x in text)):
        return True
    else:
        return False

# Set up database
#create_engine('postgresql+psycopg2://user:password@hostname/database_name')
engine = create_engine("postgresql+psycopg2://lbzjufkvjvtebx:793b53af15d23defb4713e24382f3bbd4bcbb3c9fa49fa5185421eaaa16bcc29@ec2-54-221-237-246.compute-1.amazonaws.com/dfoooegurrluke")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("welcome.html")

@app.route("/log_in")
def log_In():
    return render_template("loginPage.html")


@app.route("/register")
def sign_up():
    return render_template("signupPage.html")

@app.route("/addUser", methods=["POST"])
def add_user():
    id = request.form.get("ID")
    password = request.form.get("password")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    print(hashPassword(password))
    print(id)
    if(isValid(password) == False):
        print("Nope")
        flash('Invalid Password')
        return redirect(url_for('sign_up'))

    hashedPassword = hashPassword(password)
    #db.execute("INSERT INTO books (id, title, author, format, price) VALUES (:id, :title, :author, :format, :price)", {'id':i, 'title':tit,'author':auth,'format':form,'price':pri})

    db.execute("INSERT INTO book_user (user_id, password, first_name, last_name) VALUES (:idd, :passwordd, :first_namee, :last_namee)", {'idd': id, 'passwordd': hashedPassword, 'first_namee':first_name, 'last_namee': last_name})
    db.commit()
    #db.execute("INSERT INTO BOOK_USER (user_id, password, first_name, last_name) VALUES (:id, :hashedPassword, :first_name, :last_name)", {'id': id, 'hashedPassword':hashedPassword, 'first_name':first_name, 'last_name':last_name})

    return render_template("success.html", message="You have successfully signed up.")

@app.route("/book_page", methods=["POST", "GET"])
def authenticate():
    id = request.form.get("ID")
    password = request.form.get("Password")
    # print(id)
    # print(password)
    # if(db.execute("SELECT password FROM book_user WHERE user_id=:id", {'id':id}).fetchone()[0]==hashPassword(password)):
    #     return render_template("error.html", message="Website under construction")

    if(hashPassword(password) == db.execute("SELECT password FROM book_user WHERE user_id=:id", {'id':id}).fetchone()[0]):
        session['user'] = id
        books = db.execute("SELECT * FROM BOOKS").fetchall()
        return render_template("bookPage.html", books=books)

    flash('Incorrect Password')
    return render_template("loginPage.html")


@app.route("/book_page/<string:isbn>", methods=["GET"])
def book(isbn):
    books = db.execute("SELECT * FROM BOOKS WHERE isbn=:Isbn", {'Isbn':isbn}).fetchone()
    return render_template("book.html", book=books)





