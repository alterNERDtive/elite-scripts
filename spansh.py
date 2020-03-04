#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse
import requests
import sys

# ===========================================================================

def getOldStations(count, systemsonly):
  url = "http://backend3.spansh.co.uk:3000/api/stations/search"
  params = {"json": '{"filters":{"updated_at":{"value":["2017-11-06","2019-03-01"],"comparison":"<=>"}},"sort":[{"updated_at":{"direction":"asc"}}],"size":' + str(count)  + '}'}

  json = requests.post(url, params).json()

  ret =""

  if systemsonly:
    for station in json["results"]:
      ret += "{}\n".format(station["system_name"])
  else:
    for station in json["results"]:
      ret += "{}: {} ({})\n".format(station["system_name"], station["name"],
        station["updated_at"])

  return ret[:-1]

def getOldStationsInSystem(system):
  url = "http://backend3.spansh.co.uk:3000/api/stations/search"
  params = {"json": '{"filters": {"system_name": {"value": "' + system + '"},"updated_at":{"value":["2017-11-06","2019-03-01"],"comparison":"<=>"}},"sort":[{"updated_at":{"direction":"asc"}}]}'}

  json = requests.post(url, params).json()

  ret =""

  for station in json["results"]:
    ret += "{}, ".format(station["name"])

  return ret[:-2]

# ===========================================================================

parser = argparse.ArgumentParser(description="Script for interfacing with "
    + "Spansh’s API.")
subparsers = parser.add_subparsers(title="subcommands", help="sub-command help",
    dest="subcommand", required=True)

parser_oldstations = subparsers.add_parser("oldstations",
    help="Searches for stations with old data (>1 year without an update.")
parser_oldstations.add_argument("--system", nargs="?",
    help="a single system to query. If not present, get the oldest stations "
        + "overall.")
parser_oldstations.add_argument("--count", nargs="?", type=int, default=50,
    help="how many stations to output. Defaults to 50.")
parser_oldstations.add_argument("--systemlist", action='store_true',
    help="outputs a list of systems to visit _only_, no station names (for)"
        + "easy system names c&p")

argcomplete.autocomplete(parser)
args = parser.parse_args()

# ===========================================================================

out =""
if args.subcommand == "oldstations":
  if args.system:
    out = getOldStationsInSystem(args.system)
  else:
    out = getOldStations(args.count, args.systemlist)

if out == "":
  sys.exit(3)
else:
  print(out)
  sys.exit(0)
