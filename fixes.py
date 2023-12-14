from sqlalchemy import func
from db import db
from sqlalchemy.sql import text
import users


def get_list():
    sql = text("SELECT fixes.fixcomment, users.name, fixes.sent_at FROM fixes JOIN users ON fixes.user_id = users.id ORDER BY fixes.id;")
    result = db.session.execute(sql)
    return result.fetchall()

def sendfix(fixcomment):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO fixes (fixcomment, user_id, sent_at) VALUES (:fixcomment, :user_id, NOW())")
    db.session.execute(sql, {"fixcomment": fixcomment, "user_id": user_id, "sent_at": func.now()})
    db.session.commit()


    return True



