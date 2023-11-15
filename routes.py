from app import app
from flask import render_template, request, redirect
import first
import users
##muutki pyt pitää importtaa jos on liikettä


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 2 or len(username)>20:
            return render_template("error.html", message ="tunnuksessa tulee olla 2-20 merkkiä")
        
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if password1 =="":
            return render_template("error.html", message="Salasana ei voi olla tyhjä")
        
        ##if not users.register(username, password1):
        ##    return render_template("error.html", message = "rekisteröinti ei onnistunut")
  
    
@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    if not users.login(username, password):
        return render_template("error.html", message="Väärä tunnus tai salasana")
    return redirect("/login")

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