from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_security import login_required, login_user, logout_user, current_user, roles_accepted
from werkzeug.utils import secure_filename

from .forms import PhotoForm

from app import app
from app import db
from app import log
from app.models import *

import os

photos = Blueprint('photos', __name__, template_folder='templates')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@photos.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_info(slug):
    photo = Photo.query.filter(Photo.id==slug).first()
    form = PhotoForm(formdata=request.form, obj=photo)

    if form.validate_on_submit():
        photo.photo_title = form.photo_title.data
        photo.photo_description = form.photo_description.data
        try:
            photo.tags.append(Tag.query.filter_by(name=form.tags.data).first())
            log.debug("Photo before db '%s'." % (photo))
            db.session.commit()
            flash('Your photo edited')

            photo = Photo.query.filter(Photo.id==slug).first()
            log.debug("Photo after db '%s'." % (photo))
            tags = photo.tags
            log.info("User '%s' edit photo info '%s'." % (current_user.username, photo.photo_title))
            return render_template('photos/photo_detail.html', photo=photo, tags=tags, user=current_user)
        except:
            redirect('photos.index') 
    form = PhotoForm(obj=photo)
    return render_template('photos/edit_info.html', form=form)           

@photos.route('/', methods=['GET', 'POST'])
@login_required
def index():
    args = {'method': 'GET'}
    # MAX_FILE_SIZE = 1024 * 1024 + 1

    user = User.query.filter(User.username == current_user.username).first()     
    user_dir = user.username + user.timestamp
    user_folders = os.path.join('user_data', user_dir, 'photos')
    photos = Photo.query.filter(Photo.photo_author==current_user).all()

    friends_photo = []
    for user_ in user.followers:
        friends_photo.append(Photo.query.filter(Photo.photo_author==user_).all())

    if request.method == 'POST':       
        for file in request.files.getlist('file'):
            filename =  secure_filename(file.filename)
            # if bool(file.filename):
            #     file_bytes = file.read(MAX_FILE_SIZE)
            #     args['file_size_error'] = len(file_bytes) == MAX_FILE_SIZE
            # args['method'] = 'POST'
            #destination = '/'.join([user_folders, filename])
            destination = os.path.join('app', 'static', user_folders, filename)
            if allowed_file(filename):
                file.save(destination)

                photo = Photo(
                photo_title=filename, 
                photo_description='', 
                slug='user_data/{}/{}/{}'.format(user_dir, 'photos', filename),
                photo_author=current_user, 
                )
                db.session.add(photo)
                db.session.commit()
            else:
                flash('Not allowed file extensions')
            return redirect(url_for('photos.index'))
        return redirect(url_for('photos.index'))
    return render_template('photos/index.html', args=args, photos=photos, user=user, friends_photo=friends_photo)
    

@photos.route('/<id>')
@login_required
def photo_detail(id):
    photo = Photo.query.filter(Photo.id==id).first()
    tags = photo.tags
    return render_template('photos/photo_detail.html', photo=photo, tags=tags, user=current_user)

@photos.route('/<id>/<username>')
@login_required
def save_photo(id, username):
    photo = Photo.query.filter(Photo.id==id).first()
    tags = photo.tags
    user = User.query.filter(User.username==username).first()
    if photo not in user.save_photo:
        user.save_photo.append(photo)
    db.session.commit()
    return render_template(
        'photos/photo_detail.html', photo=photo, tags=tags, user=user, current_user=current_user)

@photos.route('/tag/<slug>')
@login_required
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first()
    photos = tag.photos_tags.all()
    return render_template('photos/tag_detail.html', tag=tag, photos=photos)
