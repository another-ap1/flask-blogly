from models import User, Post, Tag, PostTag, db
from app import app

"""Creating tables and also delteing if there is any"""
with app.app_context():
    db.drop_all()
    db.create_all()
    User.query.delete()

"""adding default users"""
grant = User(first_name="Grant", last_name="Bollaert")
alicia = User(first_name="Alicia", last_name="Bollaert")
charlotte = User(first_name="Charlotte", last_name="Bollaert")
emilia = User(first_name="Emilia", last_name="Bollaert")

"""adding default posts"""
P1 = Post(title="First post", content="I dont want to work, I just want to bang on this mug all day", user_id=1)
P2 = Post(title="First Post", content="Sometimes I dont know where im going with a sentance", user_id=2)
P3 = Post(title="First Post", content="I just got promoted to assistant to the reginal manager", user_id=3)
P4 = Post(title="First Post", content="Bears, beets, battle star galactica", user_id=4)

with app.app_context():
    db.session.add_all([grant, alicia, charlotte, emilia])
    db.session.add_all([P1, P2, P3, P4])
    db.session.commit()
