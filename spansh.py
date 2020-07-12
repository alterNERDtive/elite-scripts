#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse
import json as JSON
import requests
import sys

from datetime import datetime, timedelta, timezone
from dateutil import parser as dtparser

from pyEDSM.edsm.exception import ServerError, NotFoundError

# ===========================================================================

def querystations(url, params):
  response = requests.post(url, params)
  if response.status_code != 200:
    raise ServerError(url, params)
  json = response.json()
  if json["count"] == 0:
    raise NotFoundError()
  return json

# ===========================================================================

def getNearestSystem(coords):
  params = {
      "x": coords[0],
      "y": coords[1],
      "z": coords[2]
      }
  response = requests.post(APIURLS["nearest"], params)
  if response.status_code != 200:
    raise ServerError(url, params)

  json = response.json()

  ret = None
  system = json["system"]
  if args.short:
    ret = system["name"]
  elif args.parsable:
    ret = "{}|{},{},{}|{}".format(system["name"], system["x"],
        system["y"], system["z"], round(system["distance"], 2))
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
  json = querystations(APIURLS["stations"], params)

  ret = ""
  for station in json["results"]:
    if args.short:
      ret += "{}\n".format(station["system_name"])
    else:
      ret += "{}: {} ({} days ago)\n".format(station["system_name"], station["name"],
        (datetime.now(timezone.utc) - dtparser.parse(station["updated_at"])).days)

  return ret[:-1]

def getOldStationsInSystem(system):
  FILTERS.update(system_name={"value": system})
  params = {
      "json": JSON.dumps({
        "filters": FILTERS,
        "sort": SORT
        })
      }
  json = querystations(APIURLS["stations"], params)

  ret = ""
  for station in json["results"]:
    # systems including the given name as a word will also trigger;
    # looking for e.g. “Mari” will also give you stuff in “Mac Mari”!
    if station["system_name"] == system:
      if args.short:
        ret += "{}\n".format(station["name"])
      else:
        ret += "{} ({} days ago)\n".format(station["name"],
          (datetime.now(timezone.utc) - dtparser.parse(station["updated_at"])).days)

  return ret[:-1]

def systemExists(system):
  params = {
      "json": JSON.dumps({
        "filters": {
          "name": {
            "value": system
            }
          }
        })
      }
  response = requests.post(APIURLS["systems"], params)
  if response.status_code != 200:
    raise ServerError(url, params)

  json = response.json()
  if json["count"] == 0:
    raise NotFoundError()

  ret = ""
  for system in json["results"]:
    ret += "{} ({}, {}, {})\n".format(system["name"], system["x"], system["y"],
        system["z"])

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
group = parser_nearestsystem.add_mutually_exclusive_group(required=False)
group.add_argument("--short", action='store_true',
    help="short output format (system name only)")
group.add_argument("--parsable", action='store_true',
    help="parsable output format (<name>|<x>,<y>,<z>|<distance>)")

parser_oldstations = subparsers.add_parser("oldstations",
    help="Searches for stations with old data (>1 year without an update.")
parser_oldstations.add_argument("--system", nargs="?",
    help="a single system to query. If not present, get the oldest stations "
    + "overall.")
parser_oldstations.add_argument("--count", nargs="?", type=int, default=50,
    help="how many stations to output. Defaults to 50.")
parser_oldstations.add_argument("--minage", nargs="?", type=int, default=365,
    help="minimum age of data (in days) to be considered “outdated”. Defaults to "
    + "365 (= 1 year).")
parser_oldstations.add_argument("--short", action='store_true',
    help="short output format (system/station names only)")

parser_systemexists = subparsers.add_parser("systemexists",
    help="Checks if a given system exists in the search database.")
parser_systemexists.add_argument("system", nargs=1,
    help="the system to search for")

argcomplete.autocomplete(parser)
args = parser.parse_args()

# ===========================================================================

APIURLS = {
    "nearest": "https://spansh.co.uk/api/nearest",
    "stations": "https://spansh.co.uk/api/stations/search",
    "systems": "https://spansh.co.uk/api/systems/search",
    }

try:
  if args.subcommand == "nearestsystem":
    out = getNearestSystem(args.coordinate)
  elif args.subcommand == "oldstations":
    FILTERS = {
        "updated_at":
        {
          "value": [
            "2017-11-06",
            (datetime.now() - timedelta(days=args.minage)).strftime("%Y-%m-%d")
            ],
          "comparison": "<=>"
          }
        }
    SORT = {
        "updated_at": {
          "direction": "asc"
          }
        }
    if args.system:
      out = getOldStationsInSystem(args.system)
    else:
      out = getOldStations()
  elif args.subcommand == "systemexists":
    out = systemExists(args.system)
except ServerError as e:
  print(e)
  sys.exit(1)
except NotFoundError as e:
  print("No results found.")
  sys.exit(3)
else:
  print(out)
  sys.exit(0)
