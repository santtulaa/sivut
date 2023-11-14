import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash

def register(name, password):
    hash_value = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (name, password,)
                 VALUES (:name, :password,)"""
        db.session.execute(sql, {"name":name, "password":hash_value})
        db.session.commit()
    except:
        return False
    ##return login(name, password)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)