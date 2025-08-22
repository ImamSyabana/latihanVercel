from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import BlogPost, User

@app.route('/')
def get_all_posts():
    # data yang ada di tabel blog_posts
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()

    # data yang ada di tabel user
    
    user_results = db.session.execute(db.Select(User))
    users = user_results.scalars().all()

    return render_template("index.html", all_posts=posts, users = users)


