from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_security import login_required, login_user, logout_user, current_user, roles_accepted

from .forms import PostForm

from app import app
from app import db
from app import log
from app.models import *

posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'user')
def edit_post(slug):
    post = Post.query.filter(Post.slug==slug).first()
    form = PostForm(formdata=request.form, obj=post)
    print('edited', form.validate_on_submit())
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        try:
            post.tags.append(Tag.query.filter_by(name=form.tags.data).first())
            db.session.commit()
            flash('Your post edited')
            log.info("User '%s' edit post '%s'." % (current_user.username, post.title))
            return redirect(url_for('posts.post_detail', slug=post.slug))
        except:
           redirect('posts.index') 
    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', form=form)


@posts.route('/user_posts/<username>', methods=['GET', 'POST'])
@login_required
def user_posts(username):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            body=form.body.data,
            author=current_user,
        )
        try:
            post.tags.append(Tag.query.filter_by(name=form.tags.data).first())
            post.post_to_me.append(User.query.filter(User.username == form.post_to_me.data).first())

            db.session.add(post)
            db.session.commit()
            flash('Your post is now live!')
            return redirect(url_for('posts.index'))
        except:
            redirect('posts.user_posts')

    user = User.query.filter(User.username == username).first()
    posts = Post.query.filter(Post.author == user)
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)

    pages = posts.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])
    # max pages = posts.count() or 404
    return render_template('posts/user_posts.html', pages=pages, user=user, form=form)

@posts.route('/', methods=['GET', 'POST'])
@login_required
def index():
    users = User.query.all()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            body=form.body.data,
            author=current_user,
        )
        try:
            post.tags.append(Tag.query.filter_by(name=form.tags.data).first())
            if form.post_to_me.data != 'All':
                post.post_to_me.append(User.query.filter(User.username==form.post_to_me.data).first())

            db.session.add(post)
            db.session.commit()
            flash('Your post is now live!')
            return redirect(url_for('posts.user_posts'))
        except:
            redirect('posts.user_posts')

    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    if q:
        posts = Post.query.filter(
            ((Post.post_to_me == 'All') | (Post.post_to_me is None) ) & (
                    Post.title.contains(q) | Post.body.contains(q).all()))
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])
    return render_template('posts/index.html', users=users, form=form, pages=pages)

@posts.route('/<slug>')
@login_required
def post_detail(slug):
    post = Post.query.filter(Post.slug==slug).first()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags, user=current_user)

@posts.route('/<slug>/<username>')
@login_required
def save_post(slug, username):
    post = Post.query.filter(Post.slug==slug).first()
    tags = post.tags
    user = User.query.filter(User.username==username).first()
    if post not in user.save_post:
        user.save_post.append(Post.query.filter(Post.slug==slug).first())
    db.session.commit()
    return render_template(
        'posts/post_detail.html', post=post, tags=tags, user=user, current_user=current_user, user_posts=user.save_post)

@posts.route('/tag/<slug>')
@login_required
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first()
    posts = tag.posts_tags.all()
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)
