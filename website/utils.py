from io import BytesIO
import os
from random import Random
import random
from typing import Optional
from PIL import Image, ImageFile
from flask.helpers import make_response, send_file
from flask.wrappers import Response
from requests import get
from .models import User, Post

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

BOTTOM_WORDS_LIST = [
    'vdsdhh', 'hasj', 'xcvhr', 'hjjghf', 'nhas', 'djfn', 'gdxj', 'f', ' god ',
    'ja', ' fd', ' gaihjs'
]

BRISKET_WORDS = open(f'{STATIC_DIR}/words.txt').readlines()

def get_bottom_string(seed: Optional[int] = None) -> str:
    rng = Random(seed)
    return ''.join(rng.choice(BOTTOM_WORDS_LIST) for _ in range(5))

def get_brisket_string() -> str:
    brisket_word = random.choice(BRISKET_WORDS)
    brisket_word = brisket_word.strip()
    return brisket_word

def image_response(img: Image.Image) -> Response:
    data = BytesIO()
    img.save(data, 'PNG')
    data.seek(0)
    response = make_response(send_file(data, 'image/png'))
    response.headers['Cache-Control'] = 'no-store'
    return response

def get_image(url: str, **kw) -> Image.Image:
    with get(url, **kw) as req:
        parser = ImageFile.Parser()
        for chunk in req.iter_content(1024):
            parser.feed(chunk)
        return parser.close()

def load_user(id_):
        return User.query.get(int(id_))

def load_posts(user: int = None): #Does not work with optional (?)
        if user is None:
            return Post.query.all()
        else:
            return Post.query.filter_by(user_id=user)

def load_pfp_dir(id_):
        user = User.query.get(int(id_))
        if user.pfp == None:
            return "/static/pfps/default-pfp.png"
        else:
            return f'/static/pfps/custom/{user.pfp}'

def escape_html(htmlstring):
    escapes = {'\"': '&quot;',
               '\'': '&#39;',
               '<': '&lt;',
               '>': '&gt;'}
    # This is done first to prevent escaping other escapes.
    htmlstring = htmlstring.replace('&', '&amp;')
    for seq, esc in escapes.items():
        htmlstring = htmlstring.replace(seq, esc)
    return htmlstring