from flask import render_template, request, redirect, url_for, flash, Blueprint
from app import db
from app.models import BlogPost, User

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


