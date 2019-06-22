#! /usr/bin/env python3
import json, csv, os, re, time, random, logging, tempfile, zipfile, shutil, datetime
from urllib.request import Request
import urllib.parse
import lxml.html
from collections import OrderedDict
from tqdm import tqdm

from data import DATA, PRELOAD_IMAGES
from structures import Link
from pgi_downloader import PGIDownloader
import requests
import logging


class PGIRecord:
    """Encapsulate Cave Information from PGI portal"""

    DATA_PATH = "data/{id}.html"

    @property
    def icon(self):
        length = self.description.get('DLUGOSC', 0)

        if length < 10:
            return "#z-ico08.png"
        elif length < 100:
            return "#z-ico13.png"
        elif length < 1000:
            return "#z-ico18.png"
        return "#z-ico03.png"

    def __init__(self, id, description, *, attachments=None, links=None, coords=None):
        self.id = id
        self.description = description
        self.coords = coords or self.parse_wsg84(description.get('Współrzędne WGS84'))
        self.attachments = []
        self._preload_attachments(attachments or [])

        self.links = links or []

    @staticmethod
    def parse_wsg84(text):
        try:
            lon, lat = re.findall('(\d+)°(\d+)′(\d+(?:\.\d+)?)″', text.replace(',', '.'))
            assert (len(lat) == 3) and (len(lon) == 3)

            lat = float(lat[0]) + (float(lat[1]) + float(lat[2])/60)/60
            lon = float(lon[0]) + (float(lon[1]) + float(lon[2])/60)/60

            return (lat, lon)
        except ValueError:
            return None

    def _preload_attachments(self, ids):
        for attachment_id in ids:
            logging.debug('Preloading %s', attachment_id)
            path = f"./data/{attachment_id}.jpg"
            self.attachments.append(PGIDownloader.download(attachment_id, path))

    @classmethod
    def _preload_html(cls, id):
        path = cls.DATA_PATH.format(id=id)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'w') as output:
            r = requests.get(f"http://jaskiniepolski.pgi.gov.pl/Details/Information/{id}")
            output.write(r.text)

    @classmethod
    def load(cls, id):
        """Parse content of PGI info page, e.g. http://jaskiniepolski.pgi.gov.pl/Details/Information/406"""
        data_path = cls.DATA_PATH.format(id=id)

        if not os.path.exists(data_path):
            cls._preload_html(id)
            time.sleep(2)

        with open(data_path) as file:
            doc = lxml.html.parse(file)
            data = OrderedDict()
            for e in doc.xpath('//tr'):
                assert len(e.getchildren()) == 2
                key, value = e.getchildren()
                key = key.text_content()
                value = value.text_content()
                data[clear_text(key)] = clear_text(value)

            # Read attachments
            file.seek(0)
            text = file.read()

            if id in PRELOAD_IMAGES:
                attachments = list(map(int, re.findall('showImageInfo\((\d+)\)', text)))
                logging.info('Preloading %d images for %s', len(attachments), data['Nazwa'])
            else:
                attachments = None

            # Get Links
            links = [Link('Pokaż oryginał', f"http://jaskiniepolski.pgi.gov.pl/Details/Information/{id}")]
            if 'geostanowiska.pgi.gov.pl' in text:
                geostanowisko = re.search(r'https?://geostanowiska.pgi.gov.pl/[^"\']+', text)
                assert geostanowisko
                # print(geostanowisko, geostanowisko.group())
                links.append(Link('Geostanowisko', geostanowisko.group()))

            for content in DATA.get(id, []):
                if isinstance(content, Link):
                    links.append(content)


        return PGIRecord(
            id=id,
            description=data,
            attachments=attachments,
            links=links
        )


def query(x0, y0, x1, y1):
    print(f"query: {x0}, {y0}, {x1}, {y1}")
    params = {
        'returnGeometry': 'false',
        'where': '1=1',
        'outSr': '4326',
        'outFields': '*',
        'geometry': f"{x0},{y0},{x1},{y1}",
        'geometryType': 'esriGeometryEnvelope',

        # geometry=24.0380859375%2C49.35375571830993
        # geometryType=esriGeometryPoint
        # spatialRel=esriSpatialRelIntersects
        # units=esriSRUnit_Meter
        # distance=62840.38716486637
        'inSr': '4326',
        'f': 'json',
        # maxAllowableOffset=0.01
    }

    query_string = urllib.parse.urlencode(params)
    url = f"http://cbdgmapa.pgi.gov.pl/arcgis/rest/services/jaskinie/MapServer//0/query?{query_string}"

    with urllib.request.urlopen(url) as response:
        data = response.read()
        j = json.loads(data)
        f = j['features']
        objs = {obj['attributes']['ID']: obj['attributes'] for obj in f}
        if len(f) == 1000:
            raise OverflowError
        return objs


def get(x0, y0, x1, y1):
    try:
        resp = query(x0, y0, x1, y1)
    except OverflowError:
        sx = (x0 + x1) / 2
        sy = (y0 + y1) / 2
        r1 = get(x0, y0, sx, sy)
        r2 = get(sx, y0, x1, sy)
        r3 = get(x0, sy, sx, y1)
        r4 = get(sx, sy, x1, y1)
        resp = {**r1, **r2, **r3, **r4}

    return resp

def export_to_tsv(path, data):
    values = list(data.values())
    fieldnames = list(values[0].keys())

    with open(path, 'w') as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for item in values:
            writer.writerow(item)

def clear_text(text):
    return re.sub('\s+', ' ', text).strip()


def render_placemark(record, external_data=True):
    data = record.description
    description = []
    for key, value in data.items():
        if value.strip() == '':
            value = '---'

        description.append(f"<b>{key.upper()}</b><p>{value}</p>")
    description = "\n".join(description)

    links_html = ''.join(map(lambda link: f"<li>{link.to_html()}</li>", record.links))

    # Generate
    if record.attachments and external_data:
        attachments = "".join(map(lambda attachment: f"<lc:attachment>files/{attachment.id}.jpg</lc:attachment>", record.attachments))
        extended_data = f'<ExtendedData xmlns:lc="http://www.locusmap.eu">{attachments}</ExtendedData>'
    else:
        extended_data = ''

    html = f"""
        <Placemark>
          <name>{data['Nazwa']}</name>
          <description><![CDATA[
            <style type="text/css">p{{margin-top:0;text-align:justify}}</style>
            <small>{description}<b>LINKI</b><ul>{links_html}</ul></small><br/>
          ]]></description>
          <styleUrl>{record.icon}</styleUrl>
          {extended_data}
          <Point>
            <coordinates>{record.coords[1]},{record.coords[0]}</coordinates>
          </Point>
        </Placemark>
    """

    return ''.join([line.strip() for line in html.split("\n")])



def export_to_kml(path, data):
    attachments = []
    with open(path, 'w') as output:
        output.write("""<?xml version="1.0" encoding="utf-8"?>
            <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
            <Document>
        	<name>Jaskinie Polskie</name>
        	<atom:author><atom:name>Locus (Android)</atom:name></atom:author>
        """)

        for key, values in tqdm(data.items()):
            record = PGIRecord.load(key)

            if record.coords is None:
                logging.warning('Skipping %s', key)
                continue

            output.write(render_placemark(record))
            attachments.extend(record.attachments)

        output.write("""
            </Document>
            </kml>
        """)

    return attachments


def export_to_kmz(path, data):
    with tempfile.TemporaryDirectory() as tmp_dir:
        print()
        attachments = export_to_kml(os.path.join(tmp_dir, 'doc.kml'), data)
        os.makedirs(os.path.join(tmp_dir, 'files'))

        for attachment in attachments:
            os.symlink(attachment.path, os.path.join(tmp_dir, 'files', f"{attachment.id}.jpg"))

        shutil.make_archive(path, 'zip', tmp_dir)
        os.rename(path+'.zip', path)

def generate_data_placeholders(data):
    print("DATA = {")
    for key in sorted(data.keys()):
        print(f"\t# {data[key]['NAZWA']} / {data[key].get('NR_INWENT')}")
        print(f"\t{key}: []")
        print()
    print("}")


if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)-15s] [%(levelname)s] %(message)s')
    logging.getLogger().setLevel('INFO')

    res = get(14.0, 49.0, 24.2, 55)

    for key in tqdm(res):
        assert key in DATA
        for link in DATA[key]:
            link.validate()

    # generate_data_placeholders(res)
    output_file = "caves.%s.kmz" % datetime.datetime.today().strftime('%Y%m%d')

    logging.info('Output file: %s', output_file)
    export_to_kmz(output_file, res)

    # export_to_tsv('output.new.tsv', res)
    # export_to_kml('output.new.kml', res)
