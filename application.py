import os

from flask import Flask, session, render_template,request, url_for
from forms import SignUpForm, LoginForm
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'project1'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    form = SignUpForm()
    return render_template('registration.html', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form) 

@app.route("/redirection", methods = ["POST"])
def redirection():

    username = request.form.get("username")
    password = request.form.get("password")
    
    print(f"{username}")
    print(f"{password}")
    print("Hello")
    db.execute("INSERT INTO users(username, password) VALUES (:username, :password)", {"username": username, "password": password})
    db.commit()
    return render_template("index.html")

@app.route("/LoggingIn", methods =["POST"])
def LoggingIn():
    username = request.form.get("username")
    password = request.form.get("password")
    
    actualPassword = db.execute("SELECT password FROM users WHERE username = :username", {"username": username}).fetchone()
    db.commit()
    print(f"{actualPassword.password}/")
    print(f"{password}/")
    if password != actualPassword.password:
        return render_template("incorrect.html", word='password')

    else:
        return render_template("homepage.html", username=username) 

@app.route("/search", methods =["POST"])
def search():
    
    value = request.form.get("value")
    print(f"{value}/")
    if db.execute("SELECT * FROM books WHERE isbn LIKE ('%' || :value || '%') OR title LIKE ('%' || :value || '%') OR author LIKE ('%' || :value || '%')", {"value": value}).rowcount == 0:
        return render_template("error.html", message='No such books')
    else:
        books = db.execute("SELECT * FROM books WHERE isbn LIKE ('%' || :value || '%') OR title LIKE ('%' || :value || '%') OR author LIKE ('%' || :value || '%')", {"value": value} ).fetchall()
        db.commit()
        
        return render_template("books.html", books=books)
    
    

@app.route("/books/<int:book_id>", methods=["GET", "POST"])
def book(book_id):
    counter = 0
    result = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    print(f"{result.title}")
    db.commit()
    if request.method =="POST":
        rating=request.form.get("rating")
        review=request.form.get("review")
        counter += 1
        return render_template("book.html",result=result,rating=rating,review=review,counter=counter)
    if result is None:
        return render_template("error.html", message="No such book.")
    else:
        return render_template("book.html", result=result)
        
            



    
