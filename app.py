"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'donttellanyone'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)


with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/')
def home_page():
    """ redirect to the list of users """

    return redirect('/users')

@app.route('/users')
def show_users():
    """show a list of the current users"""

    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('index.html', users=users)

@app.route('/users/new', methods=["GET"])
def add_user():
    """shows the page to add users to the data base """
    return render_template('adduser.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """adding users to the database"""

    firstName = request.form["first_name"]
    lastName = request.form["last_name"]
    imageUrl = request.form["image_url"] or None

    new_user = User(first_name = firstName, last_name = lastName, image_url = imageUrl)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """ showing user information """

    user = User.query.get_or_404(user_id)
    return render_template('userInfo.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """show a form to update or edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template ('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Handle the form submission for editing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")






