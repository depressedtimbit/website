
from pydoc import render_doc
from turtle import bye
from flask import Blueprint, send_file, render_template, request, flash, send_from_directory, url_for, abort
from flask_login import login_required, current_user
from .models import Post, User
from . import db
import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
import os

from werkzeug.utils import redirect, secure_filename

import website

STATIC_DIR = os.path.join(os.getcwd(), 'website', 'static')

def get_bottom_string():
    ascii_list = ['vdsdhh', 'hasj', 'xcvhr', 'hjjghf', 'nhas', 'djfn', 'gdxj', 'f', ' god ', 'ja', ' fd', ' gaihjs']
    result_str = ''.join(random.choice(ascii_list) for i in range(5))
    return result_str

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", clientip=request.remote_addr)

@views.route('/forum', methods=['GET', 'POST'])
@login_required
def Forum():
    if request.method == 'POST':
        post = request.form.get('post')
        if len(post) < 1:
            flash('post is too short!', category='error')
        else:
            new_post = Post(data=post, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('post added!', category='success')

    return render_template("forum.html", user=current_user)

@views.route('/forum/user/<user_id>')
@login_required
def user(user_id=None):
    if user_id == "me":
        return render_template("user-page.html", user_id=current_user.id)
    if user == None:
        return render_template("user-page.html", user_id=current_user.id)
    if User.query.get(int(user_id)) == None:
        abort(404)
    return render_template("user-page.html", user_id=user_id)

@views.route('/forum/upload_pfp', methods = ['GET', 'POST'])
@login_required
def upload_file():
  if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('views.user', user_id="me"))
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('views.user', user_id="me"))
        if file:
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            filename = secure_filename(file.filename)
            if filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS:
                filename = filename.rsplit('.', 1)[1]
                filename = f"{str(current_user.id)}.{filename}"
                file.save(f'{STATIC_DIR}/pfps/custom/{filename}')
                updateUser = User.query.filter_by(id=current_user.id).first()
                updateUser.pfp = filename
                db.session.add(updateUser)
                db.session.commit()

                return redirect(url_for('views.user', user_id="me"))

@views.route('/delete-post', methods=['POST'])
def delete_post():
    if request.method == 'POST':
        postid = request.form.get('postid')
        post = Post.query.get(int(postid))
        if post:
                db.session.delete(post)
                db.session.commit()
    return redirect(url_for('views.Forum'))

@views.route('/rcg/')
def rcg():
    os.getcwd()
    print(f'{STATIC_DIR}/Whitney-Book.otf')
    font = ImageFont.truetype(font=f'{STATIC_DIR}/Whitney-Book.otf', size=22)
    img = Image.open(f'{STATIC_DIR}/cuz_temp.png')
    I1 = ImageDraw.Draw(img)
    random_text = get_bottom_string()
    I1.text(xy=(78, 34), text=random_text, fill="White", font=font)
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)

    return send_file(byte_io, mimetype='image/png')

@views.route('/valhallamodfile')
def vallhallmodfile():
    
    return send_file(f'{STATIC_DIR}/data_working19_final.win')

@views.route('/toajjzwtajzwotatn/')
def troll():

    fun = random.randint(1, 5)

    if fun == 5:
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    else:
        return send_file(r"/var/www/website/website/static/qr.png")

@views.route('/crsitamasagjk/')
def xmas():
    if datetime.datetime.now() > datetime.datetime(2022, 12, 25):
        return '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/sUNKxsVONug?controls=0&amp&start=16&autoplay=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    else:
        return render_template("xmas.html")

@views.route('/bloom-birthday')
def bloom_birthday():
    return render_template("birthdayburg.html")
