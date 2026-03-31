from flask import render_template, request, redirect, session, Flask, url_for, flash
from werkzeug.utils import secure_filename
from base64 import b64encode
from models import Img
from app import app
from db import db
from users import get_user_id, register
import users, reviews, fixes
from reservations import reservation
import reservations
from urllib.parse import urlparse, urljoin  # Added for URL validation
from functools import wraps

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def is_safe_url(target):
#     """Ensures the redirect target is on the same host to prevent Open Redirects."""
#     if not target:
#         return False
#     ref_url = urlparse(request.host_url)
#     test_url = urlparse(urljoin(request.host_url, target))
#     return test_url.scheme in ('http', 'https') and \
#            ref_url.netloc == test_url.netloc

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if "user_id" not in session:
#             flash("Login required", "error")
#             return redirect(url_for("login_page", next=request.full_path))
#         return f(*args, **kwargs)
#     return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Routes ---

@app.route("/front")
# @login_required
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

        return redirect(url_for("index"))

@app.route("/", methods=["GET", "POST"])
def login_page():
    next_page = request.args.get('next') or request.form.get('next')

    if request.method == "GET":
            return render_template("login.html")

    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        if not users.login(name, password):
            return render_template("login.html")
        
        return redirect("/front")
    #     return render_template("login.html", next=next_page)

    # if request.method == "POST":
    #     name = request.form["name"]
    #     password = request.form["password"]

    #     if not users.login(name, password):
    #         flash("Invalid username or password")
    #         return render_template("login.html", next=next_page)
        
        # VALIDATION: Only redirect to next_page if it is local/safe
        # if not next_page or not is_safe_url(next_page):
        #     return redirect(url_for("index"))
        
        return redirect(next_page)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/reserve", methods=["POST"])
def reserve():
    todo = request.form.get("todo")
    date = request.form.get("date")
    reservations.send(todo, date)
    return redirect(request.referrer or url_for("calendar"))

@app.route("/calendar")
# @login_required
def calendar():
    list = fixes.get_list()
    res_list = reservation()

    if res_list is not False:
        return render_template("calendar.html", events=res_list, fixmessages=list)
    else:
        return render_template("error.html", message="Error retrieving reservations from the database")

@app.route("/send", methods=["POST"])
def send():
    # Note: You should call users.check_csrf() here once you implement the hidden input in your HTML
    content = request.form["content"]
    if reviews.send(content):
        return redirect("/front")
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
# @login_required
def review():
    return render_template("review.html")

@app.route('/upload', methods=['GET', 'POST'])
# @login_required
def upload():
    if request.method == 'GET':
        return render_template('show_photos.html')

    pic = request.files.get('pic')

    if pic and allowed_file(pic.filename):
        filename = secure_filename(pic.filename)
        img_data = pic.read()

        img = Img(img=img_data, name=filename, mimetype=pic.mimetype)
        db.session.add(img)
        db.session.commit()

        return redirect(url_for('show_photos'))
    else:
        return render_template('error.html', message='Invalid file type. Please upload a valid image file.')

@app.route('/show_photos')
# @login_required
def show_photos():
    images = Img.query.all()
    template_context = {
        'images': images,
        'b64encode': b64encode  
    }
    return render_template('show_photos.html', **template_context)