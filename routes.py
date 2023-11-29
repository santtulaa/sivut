from app import app
from flask import render_template, request, redirect, session
from users import get_user_id
import users, reviews
from reservations import reservation
import reservations

##muutki pyt pitää importtaa jos on liikettä


@app.route("/")
def index():
    list = reviews.get_list()
    return render_template("index.html", messages=list)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        name = request.form["name"]
        if len(name) < 2 or len(name) > 20:
            return render_template("error.html", message="tunnuksessa tulee olla 2-20 merkkiä")
        
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return render_template("register.html")
        if password1 == "":
            return render_template("register.html")
        
        if not users.register(name, password1):
            return render_template("resgister.html")

        session["user_id"] = get_user_id(name)  
        session["user_name"] = name

        return redirect("/")
    
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

    if not users.login(name, password):
        return render_template("login.html")
    return redirect("/")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/calendar")
def calendar():

    reservations = reservation()

    if reservations is not False:
        return render_template("calendar.html", events=reservations)
    else:
        return render_template("error.html", message="Error retrieving reservations from the database")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if reviews.send(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")
    
@app.route("/review")
def review():
    return render_template("review.html")

@app.route("/reserve", methods=["POST"])
def reserve():
    todo = request.form.get("todo")
    date = request.form.get("date")
    reservations.send(todo, date)
    return redirect(request.referrer)