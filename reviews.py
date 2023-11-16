from sqlalchemy import func
from db import db
from sqlalchemy.sql import text
import users
from datetime import datetime


def get_list():
    sql = text("SELECT reviews.comment, users.name, reviews.sent_at FROM reviews JOIN users ON reviews.user_id = users.id ORDER BY reviews.id;")
    result = db.session.execute(sql)
    return result.fetchall()

def send(comment):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO reviews (comment, user_id, sent_at) VALUES (:comment, :user_id, NOW())")
    db.session.execute(sql, {"comment": comment, "user_id": user_id, "sent_at": func.now()})
    db.session.commit()


    return True



