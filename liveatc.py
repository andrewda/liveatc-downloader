import re

import requests
import urllib.request
from bs4 import BeautifulSoup


def get_stations(icao):
  page = requests.get(f'https://www.liveatc.net/search/?icao={icao}')
  soup = BeautifulSoup(page.content, 'html.parser')

  stations = soup.find_all('table', class_='body', border='0', padding=lambda x: x != '0')
  freqs = soup.find_all('table', class_='freqTable', colspan='2')

  for table, freqs in zip(stations, freqs):
    title = table.find('strong').text
    up = table.find('font').text == 'UP'
    href = table.find('a', href=lambda x: x and x.startswith('/archive.php')).attrs['href']

    identifier = re.findall(r'/archive.php\?m=([a-zA-Z0-9_]+)', href)[0]

    frequencies = []
    rows = freqs.find_all('tr')[1:]
    for row in rows:
      cols = row.find_all('td')
      freq_title = cols[0].text
      freq_frequency = cols[1].text

      frequencies.append({'title': freq_title, 'frequency': freq_frequency})

    yield {'identifier': identifier, 'title': title, 'frequencies': frequencies, 'up': up}


def download_archive(station, date, time):
  page = requests.get(f'https://www.liveatc.net/archive.php?m={station}')
  soup = BeautifulSoup(page.content, 'html.parser')
  archive_identifer = soup.find('option', selected=True).attrs['value']

  # https://archive.liveatc.net/kpdx/KPDX-App-Dep-Oct-01-2021-0000Z.mp3
  filename = f'{archive_identifer}-{date}-{time}.mp3'

  path = f'/tmp/{filename}'
  url = f'https://archive.liveatc.net/kpdx/{filename}'
  print(url)

  urllib.request.urlretrieve(url, path)


# download_archive('kpdx_zse', 'Oct-01-2021', '0000Z')
