import json, csv, os, re, time, random, logging
from urllib.request import Request
import urllib.parse
import lxml.html
from collections import OrderedDict
from tqdm import tqdm


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
    url = f"https://cbdgmapa.pgi.gov.pl/arcgis/rest/services/jaskinie/MapServer//0/query?{query_string}"

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

def get_full_description(id):
    """Parse: http://jaskiniepolski.pgi.gov.pl/Details/Information/406"""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(f"data/{id}.html"):
        os.system(f"curl -o data/{id}.html http://jaskiniepolski.pgi.gov.pl/Details/Information/{id}")
        time.sleep(2)

    with open(f"data/{id}.html") as file:
        doc = lxml.html.parse(file)
        data = OrderedDict()
        for e in doc.xpath('//tr'):
            assert len(e.getchildren()) == 2
            key, value = e.getchildren()
            key = key.text_content()
            value = value.text_content()
            data[clear_text(key)] = clear_text(value)
        return data

def parse_wsg84(text):
    try:
        lon, lat = re.findall('(\d+)°(\d+)′(\d+(?:\.\d+)?)″', text.replace(',', '.'))
        assert (len(lat) == 3) and (len(lon) == 3)

        lat = float(lat[0]) + (float(lat[1]) + float(lat[2])/60)/60
        lon = float(lon[0]) + (float(lon[1]) + float(lon[2])/60)/60

        return (lat, lon)
    except ValueError:
        return None

def _show_placemark(id, data, coord, icon):
    description = []
    for key, value in data.items():
        if value.strip() == '':
            value = '---'

        description.append(f"<b>{key.upper()}</b><p>{value}</p>")
    description = "\n".join(description)

    html = f"""
        <Placemark>
          <name>{data['Nazwa']}</name>
          <description><![CDATA[
            <style type="text/css">p{{margin-top:0;text-align:justify}}</style>
            <small>{description}</small><br/>
            <a href="http://jaskiniepolski.pgi.gov.pl/Details/Information/{id}">Pokaż oryginał</a>]]>
          </description>
          <styleUrl>{icon}</styleUrl>
          <Point>
            <coordinates>{coord[1]},{coord[0]}</coordinates>
          </Point>
        </Placemark>
    """

    return ''.join([line.strip() for line in html.split("\n")])


def get_icon(value):
    if value is None or value < 10:
        i = 8
    elif value < 100:
        i = 13
    elif value < 1000:
        i = 18
    else:
        i = 3

    return f"#z-ico{str(i).zfill(2)}.png"


def export_to_kml(path, data):
    with open(path, 'w') as output:
        output.write("""<?xml version="1.0" encoding="utf-8"?>
            <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
            <Document>
        	<name>Ulubione</name>
        	<atom:author><atom:name>Locus (Android)</atom:name></atom:author>
        """)

        iter = tqdm(data.items())
        for key, values in iter:
            iter.set_description(str(key))
            data = get_full_description(key)
            coord = parse_wsg84(data['Współrzędne WGS84'])
            if coord is None:
                logging.info('Skipping %s', key)
                continue
            icon = get_icon(values['DLUGOSC'])
            # print(data, coord)
            output.write(_show_placemark(key, data, coord, icon))

        output.write("""
            </Document>
            </kml>
        """)

def generate_data_placeholders(data):
    print("DATA = {")
    for key in sorted(data.keys()):
        print(f"\t# {data[key]['NAZWA']} / {data[key].get('NR_INWENT')}")
        print(f"\t{key}: []")
        print()
    print("}")

res = get(14.0, 49.0, 24.2, 55)
assert len(res) >= 4394

generate_data_placeholders(res)

#export_to_tsv('output.tsv', res)
#export_to_kml('output.kml', res)
