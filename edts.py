#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse
import json as JSON
import requests
import urllib
import sys

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

def getCoords(system):
  response = requests.get(APIURLS["coords"] + urllib.parse.quote(system))
  if response.status_code != 200:
    raise ServerError(url, params)

  json = response.json()['result']

  ret = json['position']
  ret['uncertainty'] = json['uncertainty']

  return ret

# ===========================================================================

parser = argparse.ArgumentParser(description="Script for interfacing with "
    + "Alot’s hosted EDTS API.")
subparsers = parser.add_subparsers(title="subcommands", help="sub-command help",
    dest="subcommand", required=True)

parser_coords = subparsers.add_parser("coords",
    help="Searches for the approximate coordinates of a given procedurally "
      + "generated system name.")
parser_coords.add_argument("system",
    help="the system name to get coordinates for")
parser_coords.add_argument("--maxuncertainty", nargs="?", type=int,
    help="maximum accepted uncertainty, if any")

argcomplete.autocomplete(parser)
args = parser.parse_args()

# ===========================================================================

APIURLS = {
    "coords": "http://edts.thargoid.space/api/v1/system_position/"
  }

try:
  if args.subcommand == "coords":
    coords = getCoords(args.system)
    if args.maxuncertainty:
      if args.maxuncertainty < coords['uncertainty']:
        raise NotFoundError()
    out = "{},{},{}|{}".format(int(coords['x']), int(coords['y']),
        int(coords['z']), int(coords['uncertainty']))
except ServerError as e:
  print(e)
  sys.exit(1)
except NotFoundError as e:
  print("Maximum uncertainty exceeded: " + str(int(coords['uncertainty']))
      + " > " + str(args.maxuncertainty))
  sys.exit(3)
else:
  print(out)
  sys.exit(0)
