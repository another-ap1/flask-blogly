"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

default_image = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String, nullable=False, default=default_image)
    
    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")

    @property
    def full_name(self):
        """combining first and last name"""

        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):
    __tablename__='posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String,
                           nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), 
                        nullable=False)
    
class PostTag(db.Model):
    __tablename__= 'post_tags'

    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id'), primary_key=True)

class Tag(db.Model):
    __tablename__='tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    posts = db.relationship(
                            'Post',
                            secondary='post_tags', 
                            backref='tags')

    
def connect_db(app):
    """connecting to database"""

    db.app = app
    db.init_app(app)