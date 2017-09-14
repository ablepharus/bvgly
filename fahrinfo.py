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


def search_request(von, nach, zeit=datetime.datetime.now()):
    ''' send a search request for a connection from `von` to `nach` at
        `zeit` account
    '''
    zeit = zeit + datetime.timedelta(hours=1)
    _init = init()
    _init = _init.replace('dox?', 'dn?')
    r = s.post(url + _init,
               data={
                   'REQ0HafasInitialSelection': '0',
                   'queryDisplayed': 'true',
                   'REQ0JourneyStopsS0A': von[2],
                   'REQ0JourneyStopsS0G': von[0],
                   'REQ0JourneyStopsS0ID': von[1],
                   'HWAI%3DJS%21js': 'yes',
                   'HWAI%3DJS%21ajax': 'yes',
                   'REQ0JourneyStopsZ0A': nach[2],
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

    return r


def search(von, nach, zeit=datetime.datetime.now()):
    ''' search and print connections
    '''
    r = search_request(von, nach, zeit=datetime.datetime.now())
    etree = lxml.html.fromstring(r.content)

    for i in etree.xpath('.//a[starts-with(@id, "linkDtlC")]/@href'):
        ri = s.get(url + i)
        ei = lxml.html.fromstring(ri.content)
        details  = ei.cssselect('tr.tpDetails')
        _first = lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None
        entries = []
        info = None

        print('-' * 80)
        for d in details:

            if d.xpath('@class') == ['tpDetails sectionInfo']:
                print(d.xpath('td[@class="remarks"]/span/strong/text()')[0])

            else:
                timeValue = d.xpath('normalize-space(td[@class="timeValue"]/text())')
                realTime = _first(d.xpath('td[@class="realTime"]/.//text()'))
                platform = _first(d.xpath('td[@class="platform"]/text()'))
                station = _first(d.xpath('td[@class="station"]/a/text()'))
                platform = platform if platform is not None else ''

                print(f'{station} at {timeValue}({realTime}) {platform}')

    return


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
        s1, s2 = tuple(map(search_station, sys.argv[1:3]))

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
