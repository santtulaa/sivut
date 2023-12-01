from sqlalchemy import func
from db import db
from sqlalchemy.sql import text
import users
from datetime import datetime


def reservation():
    try:
        # Your existing database insertion code here

        # Fetch reservations from the database (modify this query based on your actual database structure)
        reservations_query = text("SELECT todo, date FROM tryreservations")
        result = db.session.execute(reservations_query)
        reservations = [{"todo": row.todo, "date": row.date} for row in result]

        # Commit the changes to the database session
        db.session.commit()

        # Return the reservations
        return reservations

    except Exception as e:
        print(f"Error retrieving reservations from the database: {e}")
        return False
    
def send(todo, date):
    sql = text("INSERT INTO tryreservations (todo, date) VALUES (:todo, :date)")
    db.session.execute(sql, {"todo": todo, "date": date })
    db.session.commit()


    return True