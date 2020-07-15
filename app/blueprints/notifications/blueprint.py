from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_security import login_required, login_user, logout_user, current_user, roles_accepted

from .forms import NotificationForm

from app import app
from app import db
from app import log
from app.models import *

notifications = Blueprint('notifications', __name__, template_folder='templates')

@notifications.route('/', methods=['GET', 'POST'])
@login_required
def index():
    users = User.query.all()
    notifications = Crew.query.all()
    events = Event.query.all()
    # Device.query.filter(DeviceGroup.type != ModelType.TYPE_BLADE_SERVER).all()
    return render_template(
        'notifications/index.html', users=users, notifications=notifications, user=current_user, events=events)

# @posts.route('/user_posts', methods=['GET', 'POST'])
# @login_required
# def user_posts():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(
#             title=form.title.data, 
#             body=form.body.data, 
#             author=current_user, 
#             )
#         try:
#             post.tags.append(Tag.query.filter_by(name=form.tags.data).first())
#             db.session.add(post)
#             db.session.commit()
#             flash('Your post is now live!')
#             return redirect(url_for('posts.user_posts'))
#         except:
#             redirect('posts.user_posts') 

#     q = request.args.get('q')
#     page = request.args.get('page')
#     page = request.args.get('page', 1, type=int)
#     if q:
#         posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q).all())
#     else:
#         posts = Post.query.order_by(Post.created.desc())
        
#     pages = posts.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])
#     # max pages = posts.count() or 404
#     return render_template('posts/user_posts.html', form=form, pages=pages)

# @posts.route('/<slug>')
# @login_required
# def post_detail(slug):
#     post = Post.query.filter(Post.slug==slug).first()
#     tags = post.tags
#     return render_template('posts/post_detail.html', post=post, tags=tags, user=current_user)

# @posts.route('/tag/<slug>')
# @login_required
# def tag_detail(slug):
#     tag = Tag.query.filter(Tag.slug==slug).first()
#     posts = tag.posts_tags.all()
#     return render_template('posts/tag_detail.html', tag=tag, posts=posts)

