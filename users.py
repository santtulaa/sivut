import os
from db import db
from flask import abort, request, session
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

def register(name, password):
    hash_value = generate_password_hash(password)
    try:
        sql =text("INSERT INTO users (name, password) VALUES (:name, :password)")
        db.session.execute(sql, {"name":name, "password":hash_value})
        db.session.commit()
        return True
    
    except Exception as e:
        print(f"Error inserting into database: {e}")
        return False
    
def login(name, password):
    sql = text("SELECT id, password FROM users WHERE name=:name") 
    result = db.session.execute(sql, {"name": name}).fetchone()

    if not result:
        return False

    user_id, pw_hash = result
    if not check_password_hash(pw_hash, password):
        return False

    session["user_id"] = user_id
    session["user_name"] = name
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
     del session["user_id"]
     del session["user_name"]

def user_id():
    return session.get("user_id", 0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)


def get_user_id(name):
    sql = text("SELECT id FROM users WHERE name=:name")
    result = db.session.execute(sql, {"name": name}).fetchone()
    if result:
        return result[0]
    return None

def check_csrf():
	if session["csrf_token"] != request.form["csrf_token"]:
		abort(403)
          
def username_exists(username):
    sql = text("SELECT id FROM users WHERE name = :name")
    result = db.session.execute(sql, {"name": username}).fetchone()
    return result is not None

