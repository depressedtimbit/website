
from flask import Blueprint, send_file, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .models import Post
from . import db
import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random

from werkzeug.utils import redirect

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

@views.route('/delete-post', methods=['POST'])
def delete_post():
    if request.method == 'POST':
        postid = request.form.get('postid')
        post = Post.query.get(int(postid))
        if post:
            if post.user_id == current_user.id:
                db.session.delete(post)
                db.session.commit()
    return redirect(url_for('views.Forum'))

@views.route('/rcg/')
def rcg():

    font = ImageFont.truetype(font=r'/var/www/website/website/static/Whitney-Book.otf', size=22)
    img = Image.open(r"/var/www/website/website/static/cuz_temp.png")
    I1 = ImageDraw.Draw(img)
    random_text = get_bottom_string()
    I1.text(xy=(78, 34), text=random_text, fill="White", font=font)
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)

    return send_file(byte_io, mimetype='image/png')

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
