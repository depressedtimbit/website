from asyncio import wait_for
from genericpath import exists
import re
import tempfile
import uuid
from flask import Blueprint, make_response, send_file, render_template, request, flash, url_for, abort
from flask_login import login_required, current_user
from .models import Post, User
from . import db
from . import cache
import datetime
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import ffmpeg
from pytube import YouTube
from io import BytesIO
import random
import os

from werkzeug.utils import redirect, secure_filename

import website

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

def get_bottom_string():
    ascii_list = ['vdsdhh', 'hasj', 'xcvhr', 'hjjghf', 'nhas', 'djfn', 'gdxj', 'f', ' god ', 'ja', ' fd', ' gaihjs']
    result_str = ''.join(random.choice(ascii_list) for i in range(5))
    return result_str

views = Blueprint('views', __name__)

@views.route('/')
@cache.cached(timeout=50)
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
    font = ImageFont.truetype(font=f'{STATIC_DIR}/Whitney-Book.otf', size=22)
    img = Image.open(f'{STATIC_DIR}/cuz_temp.png')
    I1 = ImageDraw.Draw(img)
    random_text = get_bottom_string()
    I1.text(xy=(78, 34), text=random_text, fill="White", font=font)
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)

    response = make_response(send_file(byte_io, mimetype='image/png'))
    response.headers["Cache-Control"] = "no-store"
    return  response

@views.route('/valhallamodfile')
def vallhallmodfile():
    
    return send_file(f'{STATIC_DIR}/data_working19_final.win')

@views.route('/toajjzwtajzwotatn/')
def troll():

    fun = random.randint(0, 5)

    if fun == 4:
        return redirect("https://www.youtube.com/watch?v=yPYZpwSpKmA")
    elif fun == 5:
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    else:
        return send_file(os.path.join(f"{STATIC_DIR}", "qr.png"))

@views.route('/crsitamasagjk/')
def xmas():
    if datetime.datetime.now() > datetime.datetime(2022, 12, 25):
        return '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/sUNKxsVONug?controls=0&amp&start=16&autoplay=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    else:
        return render_template("xmas.html")

@views.route('/bloom-birthday')
def bloom_birthday():
    return render_template("birthdayburg.html")

@views.route('/pokemon/')
def pokemon():
    random_pokemon = random.randint(0, 905)
    random_pokemon = str(random_pokemon).rjust(3, "0")
    
    random_pokemon_url = f"https://assets.pokemon.com/assets/cms2/img/pokedex/detail/{random_pokemon}.png"
    with urllib.request.urlopen(random_pokemon_url) as url:
        pokemon_file = BytesIO(url.read())
    
    pokemon = Image.open(pokemon_file)

    pokemon = pokemon.convert("RGBA")

    jarImg = Image.open(f'{STATIC_DIR}/pokemon/jar.png')

    img = Image.new("RGBA", size=(500, 500))

    pokemon = pokemon.resize((263, 263), resample=Image.LANCZOS)
    jarImg = jarImg.resize((445, 500), resample=Image.LANCZOS)

    img.paste(pokemon, (115, 156))
    img.paste(jarImg, (28, 0), jarImg)
    
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)

    response = make_response(send_file(byte_io, mimetype='image/png'))
    response.headers["Cache-Control"] = "no-store"
    return  response

@views.route('/whos-that-pokemon/')
def whosthatpokemon():
    random_pokemon = random.randint(0, 905)
    random_pokemon = str(random_pokemon).rjust(3, "0")
    
    random_pokemon_url = f"https://assets.pokemon.com/assets/cms2/img/pokedex/detail/{random_pokemon}.png"
    with urllib.request.urlopen(random_pokemon_url) as url:
        pokemon_file = BytesIO(url.read())
    
    pokemon = Image.open(pokemon_file)

    pokemon = pokemon.convert("RGBA")

    pokemon_light = ImageEnhance.Brightness(pokemon)
    pokemon_dark = pokemon_light.enhance(0)

    background = Image.open(f'{STATIC_DIR}/pokemon/whos-that-pokemon.jpg')
    background = background.convert("RGBA")

    background.paste(pokemon_dark, (88, 45), pokemon_dark)
 
    byte_io = BytesIO()
    background.save(byte_io, 'PNG')
    byte_io.seek(0)

    response = make_response(send_file(byte_io, mimetype='image/png'))
    response.headers["Cache-Control"] = "no-store"
    return  response

@views.route('/the/<path:parseurl>')
def the(parseurl):

    tempdir = tempfile.mkdtemp(prefix="test-dir-")

    audio = os.path.join(tempdir, f"aud-{str(uuid.uuid4())}.mp3")
    image = os.path.join(tempdir, f"img-{str(uuid.uuid4())}.png")
    video = os.path.join(tempdir, f"vid-{str(uuid.uuid4())}.mp4")
   
    if request.args.get('v'): 
        parseurl = request.args.get('v')
    else:
        parseurl = str(parseurl).replace("https://youtu.be/", "")
    
    print(parseurl)

    url = f"www.youtube.com/watch?v={parseurl}"

   
    try: yt = YouTube(url=url)
    except: abort(404)

    ytvideo = yt.streams.filter(only_audio=True).first()

    ytvideo.download(filename=audio)

    background = Image.open(os.path.join(STATIC_DIR, "the.png"))
    
    thumbnailurl = yt.thumbnail_url
    with urllib.request.urlopen(thumbnailurl) as url:
        thumbnail = Image.open(BytesIO(url.read()))
    
    targetwidth = 317 / thumbnail.height * thumbnail.width

    thumbnail = thumbnail.resize((int(targetwidth), 317), Image.NEAREST)

    background.paste(thumbnail, (16, 680))

    font = ImageFont.truetype(font=os.path.join(STATIC_DIR, "Impact 400.ttf"), size=100)

    I1 = ImageDraw.Draw(background)

    n = 20
    title = ""
    title = '\n'.join(re.findall('.{1,%i}' % n, yt.title))
    
    I1.multiline_text(xy=(380, 27), text=title, fill="white", stroke_fill="black", stroke_width=5, font=font, )


    background.save(image, 'PNG')
    
    ffimage = ffmpeg.input(image)
    ffaudio = ffmpeg.input(audio)
    stream = ffmpeg.output(ffimage, ffaudio, video)
    ffmpeg.run(stream), 500
    
    return send_file(video, mimetype="video/MP4")