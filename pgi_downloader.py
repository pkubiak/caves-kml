"""
Module contains functionality for downloading images from http://jaskiniepolski.pgi.gov.pl/
"""
import os
import requests
import tempfile
import time
from PIL import Image
from io import BytesIO
from typing import NamedTuple


class PGIImage(NamedTuple):
    id: int
    path: str
    name: str


class PGIDownloader:
    IMAGE_INFO_URL = 'https://jaskiniepolski.pgi.gov.pl/Details/ImageInformation'
    IMAGE_RENDER_URL = 'http://jaskiniepolski.pgi.gov.pl/Details/RenderImage'

    @classmethod
    def _get_image_info(cls, id: int):
        req = requests.post(cls.IMAGE_INFO_URL, params=dict(id=id))
        return req.json()

    @classmethod
    def download(cls, id: int, output: str, *, force: bool = False) -> PGIImage:
        info = cls._get_image_info(id)
        
        dirname = os.path.dirname(output)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        if not os.path.isfile(output) or force:
            r = requests.get(cls.IMAGE_RENDER_URL, params=dict(id=id, zoom=0, ifGet='false', date=int(time.time())))
            time.sleep(2)
            image_data = BytesIO(r.content)

            img = Image.open(image_data)
            assert img.size[0] == info['maxWidth']
            assert img.size[1] == info['maxHeight']

            img.save(output)

        return PGIImage(id=id, path=os.path.realpath(output), name=f"{info['grafika_nazwa']} ({info['autor_nazwa']})")


if __name__ == '__main__':
    out = PGIDownloader.download(1561, "image-1561.jpg")
    print(out)
