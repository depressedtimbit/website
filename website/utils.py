from io import BytesIO
from random import Random
from typing import Optional
from PIL import Image, ImageFile
from flask.helpers import make_response, send_file
from flask.wrappers import Response
from requests import get

BOTTOM_WORDS_LIST = [
    'vdsdhh', 'hasj', 'xcvhr', 'hjjghf', 'nhas', 'djfn', 'gdxj', 'f', ' god ',
    'ja', ' fd', ' gaihjs'
]

def get_bottom_string(seed: Optional[int] = None) -> str:
    rng = Random(seed)
    return ''.join(rng.choice(BOTTOM_WORDS_LIST) for _ in range(5))

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

