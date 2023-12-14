from db import db
class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    mimetype = db.Column(db.String(50), nullable=False)