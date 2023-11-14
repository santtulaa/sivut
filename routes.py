from app import app
from flask import Flask, render_template
import first
##muutki pyt pitää importtaa jos on liikettä


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register")


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