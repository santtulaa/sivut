from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
db.create_all()

@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()