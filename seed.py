from models import User, db
from app import app

"""Creating tables"""

with app.app_context():
    db.drop_all()
    db.create_all()
    User.query.delete()

"""If table isnt empty, empty it"""


grant = User(first_name="Grant", last_name="Bollaert")
alicia = User(first_name="Alicia", last_name="Bollaert")
charlotte = User(first_name="Charlotte", last_name="Bollaert")
emilia = User(first_name="Emilia", last_name="Bollaert")

with app.app_context():
    db.session.add(grant)
    db.session.add(alicia)
    db.session.add(charlotte)
    db.session.add(emilia)

    db.session.commit()
