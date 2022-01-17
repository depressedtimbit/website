from typing import IO
from flask import Blueprint, request, render_template, send_file, Response
import time
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

@views.route('/rcg/')
def rcg():

    font = ImageFont.truetype(font=r'/home/ubuntu/website/website/static/Whitney-Book.otf', size=22)
    img = Image.open(r"/home/ubuntu/website/website/static/cuz_temp.png")
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
        return send_file(r"/home/ubuntu/website/website/static/qr.png")

@views.route('/crsitamasagjk/')
def xmas():
    if datetime.datetime.now() > datetime.datetime(2022, 12, 25):
        return '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/sUNKxsVONug?controls=0&amp&start=16&autoplay=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    else:
        return render_template("xmas.html", )

