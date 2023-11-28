import os
from db import db
from flask import abort, request, session, render_template
from sqlalchemy import text

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