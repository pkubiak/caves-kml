import logging
import requests


class Link:
    title: str
    url: str

    def __init__(self, title, url):
        self.url = url
        self.title = title

    def to_html(self):
        return f'<a href="{self.url}">{self.title}</a>'

    def validate(self):
        """Check if link is correct"""
        logging.info('Validating: %s', self.url)
        status_code = requests.head(self.url, allow_redirects=True).status_code
        if status_code != 200:
            logging.error('Validating: %s -> %d', self.url, status_code)
        # assert status_code == 200, f">> {status_code}"
        # logging.error('')


class SzkicTechnicznyKKTJ(Link):
    def __init__(self, id):
        super().__init__('Szkic Techniczny', f"https://kktj.pl/Portals/0/szkice/{id}.pdf")

class Epimenidas(Link):
    def __init__(self, id):
        super().__init__('Epimenides', f"http://www.sktj.pl/epimenides/{id}.html")

class Wikipedia(Link):
    """Link to polish wikipedia"""
    def __init__(self, id):
        super().__init__('Wikipedia', f"https://pl.wikipedia.org/wiki/{id}")

class Geocache(Link):
    """Link to geocache in geocaching.com portal"""
    def __init__(self, id):
        super().__init__('Geocaching.com', f"https://coord.info/{id}")

# class Attachment:
#     pass
#
# class AttachmentImages(Attachment):
#     """Download PGI attachments images"""
#
