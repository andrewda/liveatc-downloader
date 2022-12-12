#!/usr/bin/env python3

from cli import get_args
from liveatc import get_stations, download_archive
from datetime import datetime, timedelta

# Gets the last Zulu period of 30 minutes
# E.g. if time is 10:35:00, it will return 10:00:00
def get_last_zulu_period(date, minutes=30):
  return date - timedelta(minutes=minutes) - (date - datetime.min) % timedelta(minutes=minutes)


def stations(args):
  stations = get_stations(args.icao)
  for station in stations:
    print(f"[{station['identifier']}] - {station['title']}")

    for freq in station['frequencies']:
      print(f"\t{freq['title']} - {freq['frequency']}")

    print()


def download(args):
  date_now = datetime.utcnow()

  last_period = get_last_zulu_period(date_now)

  if not args.date and not args.time:
    date = last_period.strftime('%b-%d-%Y')
    time = last_period.strftime('%H%MZ')
  else:
    date = args.date if args.date else date_now.strftime('%b-%d-%Y')
    time = args.time if args.time else last_period.strftime('%H%MZ')

  download_archive(args.station, date, time)


if __name__ == '__main__':
  args = get_args()
  print(args)

  if args.command == 'stations':
    stations(args)
  elif args.command == 'download':
    download(args)
