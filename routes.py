from app import app
from flask import render_template, request, redirect, session
from users import register, get_user_id
import users
import first


##muutki pyt pitää importtaa jos on liikettä


@app.route("/")
def index():
    return render_template("index.html")


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
            return render_template("error.html", message="Salasanat eroavat")
        if password1 == "":
            return render_template("error.html", message="Salasana ei voi olla tyhjä")
        
        if not users.register(name, password1):
            return render_template("error.html", message="epäonnistui")

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
        return render_template("error.html", message="Väärä tunnus tai salasana")
    return redirect("/")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/calendar")
def calendar():
    return render_template("calendar.html", events = events)


events = [
    {
        "todo": "committaa",
        "date": "2023-11-14",
    },
    {
        "todo" : "sql jutut yhteen",
        "date" : "2023-11-15",
    }
]