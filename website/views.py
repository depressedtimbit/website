from typing import IO
from flask import Blueprint, request, render_template, send_file, Response
import time
import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random

from flask.helpers import total_seconds
from werkzeug.wrappers import response

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

@views.route('/crsitamasagjk/')
def xmas():
    return render_template("xmas.html", )

@views.route('/xmastimer')
def xmastimer():
    def countdown():
        td = datetime.datetime(2021, 12, 25) - datetime.datetime.now()
        hours = td.seconds // 3600
        minutes = td.seconds // 60
        
        response = f"{td.days} days {hours} hours {minutes - hours * 60} minutes {td.seconds - minutes * 60} seconds"
        return response
    return Response(countdown(), mimetype='text/html') 
