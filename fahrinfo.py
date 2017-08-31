import requests
import lxml.html
import re
import json
import sys
import datetime

s = requests.session()
url = 'https://fahrinfo.bvg.de'
base_url = 'https://fahrinfo.bvg.de'


def init():
    r = s.get('https://fahrinfo.bvg.de/Fahrinfo/'
              'bin/query.bin/dox?protocol=https:&',)
    etree = lxml.html.fromstring(r.content)
    search_url = etree.xpath('//form/@action')[0]
    return search_url


def search(von, nach, zeit=datetime.datetime.now()):
    zeit = zeit + datetime.timedelta(hours=1)
    r = s.post(url + init(),
               data={
                   'REQ0HafasInitialSelection': '0',
                   'queryDisplayed': 'true',
                   'REQ0JourneyStopsS0A': '1',
                   'REQ0JourneyStopsS0G': von[0],
                   'REQ0JourneyStopsS0ID': von[1],
                   'HWAI%3DJS%21js': 'yes',
                   'HWAI%3DJS%21ajax': 'yes',
                   'REQ0JourneyStopsZ0A': '1',
                   'REQ0JourneyStopsZ0G': nach[0],
                   'REQ0JourneyStopsZ0ID': nach[1],
                   'REQ0JourneyDate': zeit.strftime('%d.%m.%y'),
                   'HTML5_DATE': zeit.isoformat()[:10],
                   'REQ0JourneyTime': zeit.strftime('%H%M'),
                   'REQ0HafasSearchForw': '',
                   'existTotal_enable': 'yes',
                   'application': 'PRIVATETRANSPORT',
                   'REQ0Total_Foot_enable': 1,
                   'REQ0Total_Foot_minDist': 0,
                   'REQ0Total_Foot_maxDist': 2000,
                   'REQ0Total_Foot_speed': 100,
                   'REQ0Total_Bike_enable': 1,
                   'REQ0Total_Bike_minDist': 0,
                   'REQ0Total_Bike_maxDist': 10000,
                   'REQ0Total_Taxi_enable': 0,
                   'REQ0Total_Taxi_minDist': 2000,
                   'REQ0Total_Taxi_maxDist': 100000,
                   'REQ0Total_KissRide_enable': 0,
                   'REQ0Total_KissRide_minDist': 50000,
                   'REQ0Total_KissRide_maxDist': 1000000,
                   'start': 'Suchen'
           })

    etree = lxml.html.fromstring(r.content)
    connections, infos = [], []
    for href in etree.xpath('//td[starts-with(@class,con)]/a/@href'):
        if href.startswith('/Fahrinfo/bin/query'):
            connections.append(href)
        if href.startswith('/Fahrinfo/bin/query'):
            infos.append(href)

    for connection in connections:
        connection_infos(connection)


def connection_infos(url):
    r = s.get(base_url + url)
    etree = lxml.html.fromstring(r.content)

    print('-' * 80)
    for part in etree.xpath('//p[starts-with(@class,"con")]'):
        text = part.xpath('normalize-space()')
        print(text)

        # Todo
        continue
        a = [(a.xpath('./@href')[0],
              ''.join(list(a.xpath('./text()'))), a)
             for a in part.xpath('.//a')]
        for href, text, a in a:
            text = text.replace('\n', '')

            while text.find('  ') != -1:
                text = text.replace('  ', ' ')
            if href.startswith('/Fahrinfo/bin/traininfo'):
                print(f'{text}' + a.xpath('strong/text()')[0])
            elif href.find('content/standortplaene') != -1:
                print('Found Lageplan')
            elif href.startswith('/Fahrinfo/bin/help.bin/dox?tpl=streckenin'):
                print('Found info')
            elif href.find('MapLocation') != -1:
                print('Found BVG Falk - Map')
            elif href.startswith('//fahrinfo.bvg.de/Fahrinfo/bin/stboard.bin'):
                print('Found more links')
            elif text == 'Fußweg':
                print('Found Fuẞweg')
            else:
                print(f'"{text}" - {href}')

        an_ab = ''.join(part.xpath('text()')).replace('\n', '')
        an, ab = re.search('an (\d+):(\d+)', an_ab), \
                 re.search('ab (\d+):(\d+)', an_ab)
        try:
            anh, anm = an[1], an[2]
            abh, abm = ab[1], ab[2]
        except TypeError:
            m = re.search('(\d+) Min\.', an_ab)
            try:
                print(f'::: in {m[1]} minutes')
            except:
                print(f'could not parse {an_ab}')



def search_station(name):
    r = requests.get('https://fahrinfo.bvg.de/Fahrinfo/bin/'
                     'ajax-getstop.bin/dny',
                     params={
                         'start': '1',
                         'tpl': 'suggest2json',
                         'REQ0JourneyStopsS0F': 'excludeStationAttribute;FO'
                         'distinguishPerimeterFilter;13400299;52516597;10',
                         'REQ0JourneyStopsS0A': '7',
                         'getstop': '1',
                         'noSession': 'yes',
                         'REQ0JourneyStopsB': '23',
                         'REQ0JourneyStopsS0G': name,
                         'js': 'false',
                     })
    content = r.content.decode()
    j = json.loads(content[content.find('=')+1:-22])
    s = j['suggestions']
    ret = []
    for p in s:
        value, typestr, id = p['value'], p['typeStr'], p['id']
        ret.append((value, id, typestr))

    return ret


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Bitte Addressen angeben')
        sys.exit(1)
    if len(sys.argv) == 2:
        print(search_station(sys.argv[1]))
        sys.exit(0)

    if len(sys.argv) > 2:
        s1 = search_station(sys.argv[1])
        s2 = search_station(sys.argv[2])

    now = datetime.datetime.now()
    if len(sys.argv) == 4:
        arg = sys.argv[3]
        if arg.endswith('m'):
            now += datetime.timedelta(minutes=int(arg[:-1]))
        elif arg.endswith('h'):
            now += datetime.timedelta(hours=int(arg[:-1]))
        elif len(arg.split(':')) == 2:
            h, m = arg.split(':')
            now = datetime.datetime(now.year, now.month, now.day,
                                    int(h), int(m))

    search(s1[0], s2[0], now)