#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse
import json as JSON
import requests
import sys

from datetime import datetime, timedelta

# ===========================================================================

def getNearestSystem(coords):
  params = {
      "x": coords[0],
      "y": coords[1],
      "z": coords[2]
      }
  json = requests.post(APIURLS["nearest"], params).json()

  ret = ""
  if args.short:
    ret = json["system"]["name"]
  else:
    system = json["system"]
    ret = "{} ({}, {}, {}), {} ly".format(system["name"], system["x"],
        system["y"], system["z"], round(system["distance"], 2))

  return ret

def getOldStations():
  params = {
      "json": JSON.dumps({
        "filters": FILTERS,
        "sort": SORT,
        "size": args.count
        })
      }
  json = requests.post(APIURLS["stations"], params).json()

  ret =""
  for station in json["results"]:
    if args.short:
      ret += "{}\n".format(station["system_name"])
    else:
      ret += "{}: {} ({})\n".format(station["system_name"], station["name"],
        station["updated_at"])

  return ret[:-1]

def getOldStationsInSystem(system):
  FILTERS.update(system_name={"value": system})
  params = {
      "json": JSON.dumps({
        "filters": FILTERS,
        "sort": SORT
        })
      }
  json = requests.post(APIURLS["stations"], params).json()

  ret =""
  for station in json["results"]:
    if args.short:
      ret += "{}\n".format(station["name"])
    else:
      ret += "{} ({})\n".format(station["name"], station["updated_at"])

  return ret[:-1]

# ===========================================================================

parser = argparse.ArgumentParser(description="Script for interfacing with "
    + "Spansh’s API.")
subparsers = parser.add_subparsers(title="subcommands", help="sub-command help",
    dest="subcommand", required=True)

parser_nearestsystem = subparsers.add_parser("nearestsystem",
    help="Searches for the nearest system in the database to given coordinates.")
parser_nearestsystem.add_argument("coordinate", nargs=3, type=int,
    help="the coordinates to search for (order: x, y, z)")
parser_nearestsystem.add_argument("--short", action='store_true',
    help="short output format (system name only)")

parser_oldstations = subparsers.add_parser("oldstations",
    help="Searches for stations with old data (>1 year without an update.")
parser_oldstations.add_argument("--system", nargs="?",
    help="a single system to query. If not present, get the oldest stations "
    + "overall.")
parser_oldstations.add_argument("--count", nargs="?", type=int, default=50,
    help="how many stations to output. Defaults to 50.")
parser_oldstations.add_argument("--short", action='store_true',
    help="short output format (system/station names only)")

argcomplete.autocomplete(parser)
args = parser.parse_args()

# ===========================================================================

APIURLS = {
    "stations": "https://spansh.co.uk/api/stations/search",
    "nearest": "https://spansh.co.uk/api/nearest"
    }
FILTERS = {
    "updated_at":
      {
        "value": [
          "2017-11-06",
          (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        ],
        "comparison": "<=>"
      }
    }
SORT = {
    "updated_at": {
      "direction": "asc"
      }
    }

out =""
if args.subcommand == "nearestsystem":
  out = getNearestSystem(args.coordinate)
elif args.subcommand == "oldstations":
  if args.system:
    out = getOldStationsInSystem(args.system)
  else:
    out = getOldStations()
else:
  parser.print_usage(sys.stderr)
  sys.exit(1)

if out == "":
  sys.exit(3)
else:
  print(out)
  sys.exit(0)
