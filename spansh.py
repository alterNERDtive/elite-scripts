#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse
import json as JSON
import requests
import sys

from datetime import datetime, timedelta

# ===========================================================================

def getOldStations(systemsonly):
  params = {"json": JSON.dumps({"filters": FILTERS, "sort": SORT, "size": COUNT})}
  json = requests.post(APIURL, params).json()

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
  FILTERS.update(system_name={"value": system})
  params = {"json": JSON.dumps({"filters": FILTERS, "sort": SORT})}
  json = requests.post(APIURL, params).json()

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
    help="outputs a list of systems to visit _only_, no station names (for"
        + "easy system names c&p)")

argcomplete.autocomplete(parser)
args = parser.parse_args()

# ===========================================================================

APIURL = "http://backend3.spansh.co.uk:3000/api/stations/search"

FILTERS = {"updated_at":
  {"value":
    ["2017-11-06",
    (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")],
  "comparison": "<=>"}}
SORT = {"updated_at": {"direction": "asc"}}
COUNT = args.count

out =""
if args.subcommand == "oldstations":
  if args.system:
    out = getOldStationsInSystem(args.system)
  else:
    out = getOldStations(args.systemlist)
else:
  parser.print_usage(sys.stderr)
  sys.exit(1)

if out == "":
  sys.exit(3)
else:
  print(out)
  sys.exit(0)
