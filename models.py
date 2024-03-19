"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

default_image = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String, nullable=False, default=default_image)
    
    
    def full_name(self):
        """combining first and last name"""

        return f"{self.first_name} {self.last_name}"
    
def connect_db(app):
    """connecting to database"""

    db.app = app
    db.init_app(app)