"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    
    posts = Post.query.filter_by(user_id=user_id)

    return render_template('userInfo.html', user=user, posts=posts)

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

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """page for user to add a new post"""

    user = User.query.get_or_404(user_id)
    
    return render_template('newPost.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def make_post(user_id):
    """adding post and redirect to users"""

    user = User.query.get_or_404(user_id)
    
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user=user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def users_posts(post_id):
    """show a posts content"""

    #user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    
    return render_template('postDetails.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Edit a users post"""
    post = Post.query.get(post_id)

    return render_template('editPosts.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def make_edit(post_id):
    """making the edit to post and redirecting to user"""

    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Remove users post"""
    
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')