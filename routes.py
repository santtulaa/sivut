from flask import render_template, request, redirect, session, Response, Flask
from werkzeug.utils import secure_filename
import os
from app import app
from users import get_user_id
import users, reviews, fixes
from reservations import reservation

import reservations
from PIL import Image
import numpy as np

from db import db_init, db
from models import Img
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
            return render_template("register.html")

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


@app.route("/fix")
def fix():
    return render_template("fix.html")

@app.route("/reserve", methods=["POST"])
def reserve():
    todo = request.form.get("todo")
    date = request.form.get("date")
    reservations.send(todo, date)
    return redirect(request.referrer)

# @app.route('/upload', methods=['GET', 'POST'])
# def home():
#     if request.method == 'GET':
#         return render_template('upload.html', msg='')

    # image = request.files['file']
    # img = Image.open(image)
    # img = np.array(img)

    # print(img)
    # print(img.shape)

    # return render_template('photos.html', msg='Your image has been uploaded')


# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'GET':
#         return render_template('upload.html')
#     pic = request.files['pic']
#     if not pic:
#         return 'No pic uploaded!', 400

#     filename = secure_filename(pic.filename)
#     mimetype = pic.mimetype
#     if not filename or not mimetype:
#         return 'Bad upload!', 400

#     img = Img(img=pic.read(), name=filename, mimetype=mimetype)
#     db.session.add(img)
#     db.session.commit()

#     return 'Img Uploaded!', 200


# @app.route('/<int:id>')
# def get_img(id):
#     img = Img.query.filter_by(id=id).first()
#     if not img:
#         return 'Img Not Found!', 404

#     return Response(img.img, mimetype=img.mimetype)
upload_folder = os.path.join("static", "uploads")

app.config["UPLOAD"] = upload_folder

@app.route('/show_photos')
def show_photos():
    # Specify the path to your photo folder
    folder_path = os.path.join(app.static_folder, 'uploads')

    # List all image files in the folder (filter by extension)
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Render the template and pass the list of image files
    return render_template('show_photos.html', image_files=image_files)

@app.route("/image", methods=["GET", "POST"])
def image():
    if request.method == "GET":
        return render_template("image_render.html")
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        return render_template('image_render.html', img=img)
    return render_template('image_render.html')