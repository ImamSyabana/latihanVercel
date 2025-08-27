from flask import render_template, request, redirect, url_for, flash, Blueprint
from app import db
from app.models import BlogPost, User
from app.forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user,login_required

main = Blueprint('main', __name__)


@main.route('/')
def get_all_posts():
    # data yang ada di tabel blog_posts
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()

    # data yang ada di tabel user
    
    user_results = db.session.execute(db.select(User))
    users = user_results.scalars().all()

    return render_template("index.html", all_posts=posts, users = users)


# TODO: Retrieve a user from the database based on their email. 
@main.route('/login', methods = ["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        # mengambil yang ada di kolom input HTML
        email = form.email.data
        password = form.password.data

        # mengambil data user yang ada di database
        user_to_login = db.session.execute(db.Select(User).where(User.email == email)).scalar()

        # Login and validate the user.
        # user should be an instance of your `User` class
        # Check if the user exists and the password is correct
        if not(user_to_login):
            # Handle invalid credentials
            flash('That email does not exist. Please try again.', 'error')
            return redirect(url_for('login'))
        elif check_password_hash(user_to_login.password, password) == False:
            # Handle invalid credentials
            flash('Password Incorrect. Please try again.', 'error')
            return redirect(url_for('login'))
        else:
            #flash('You were successfully logged in!', 'success')
            login_user(user_to_login)
            return redirect(url_for("get_all_posts"))
        
    return render_template("login.html", form = form)


# TODO: Use Werkzeug to hash the user's password when creating a new user.
@main.route('/register', methods = ["GET", "POST"])
def register():
    form = RegisterForm()

    if request.method == "POST":
        # mengambil yang ada di kolom input HTML
        name = form.name.data
        email = form.email.data

        # convert password menjadi hash + salt
        password = form.password.data
        password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        
        user_to_register = db.session.execute(db.select(User).where(User.email == email)).scalar()
        
        # kalo email sudah exist maka user_to_register ada isinya 
        # berarti ngga boleh register
        if user_to_register:
            # Handle existed credentials
            flash('You have signed up with that email, log in instead.', 'error')
            return redirect(url_for('login'))
        
        # kalo email belum exist berarti user_to_register return None
        # berarti email belum pernah dipake dan boleh register.
        elif not(user_to_register):
            # menyiapkan records object USER untuk dimasukkan ke database
            new_user = User(
                email = email,
                password = password,
                name = name
            )

            # menambahkan data ke datatbase.
            db.session.add(new_user)
            db.session.commit()
            
            # login the new user
            login_user(new_user)

            return redirect(url_for('get_all_posts'))
    return render_template("register.html", form = form)

@main.route("/about")
def about():
    return render_template("about.html")

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))

@main.route("/contact")
def contact():
    return render_template("contact.html")