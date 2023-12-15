from flask import render_template, request, redirect, session, Flask, url_for
from werkzeug.utils import secure_filename
from base64 import b64encode
from models import Img
from app import app
from db import db
from users import get_user_id
import users, reviews, fixes
from reservations import reservation

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            return render_template("register.html")

        session["user_id"] = get_user_id(name)  
        session["user_name"] = name

        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login_page():
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
    list = fixes.get_list()
    reservations = reservation()

    if reservations is not False:
        return render_template("calendar.html", events=reservations, fixmessages=list)
    else:
        return render_template("error.html", message="Error retrieving reservations from the database")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if reviews.send(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

@app.route("/sendfix", methods=["POST"])
def sendfix():
    content = request.form["content"]
    if fixes.sendfix(content):
        return redirect("/calendar")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

@app.route("/review")
def review():
    return render_template("review.html")



@app.route("/reserve", methods=["POST"])
def reserve():
    todo = request.form.get("todo")
    date = request.form.get("date")
    reservations=reservation()
    reservations.send(todo, date)
    return redirect(request.referrer)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('show_photos.html')

    pic = request.files['pic']

    if pic and allowed_file(pic.filename):
        filename = secure_filename(pic.filename)
        img_data = pic.read()

        # Save the image to the database
        img = Img(img=img_data, name=filename, mimetype=pic.mimetype)
        db.session.add(img)
        db.session.commit()

        return redirect(url_for('show_photos'))
    else:
        return render_template('error.html', message='Invalid file type. Please upload a valid image file.')

@app.route('/show_photos')
def show_photos():
    images = Img.query.all()

    template_context = {
        'images': images,
        'b64encode': b64encode  
    }

    return render_template('show_photos.html', **template_context)
