#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse
import math
import sys

from pyEDSM.edsm.exception import ServerError, NotFoundError
from pyEDSM.edsm.models import System, Commander

# ===========================================================================

def distanceBetween(system1, system2):
  coords1 = System(system1).coords
  coords2 = System(system2).coords
  return int(round(math.sqrt( (coords1['x']-coords2['x'])**2
      + (coords1['y']-coords2['y'])**2
      + (coords1['z']-coords2['z'])**2 ),0))

def findCommander(name, apikey):
  return Commander(name, apikey).currentSystem

def getBodyCount(system):
  return System(system).bodyCount

# ===========================================================================

parser = argparse.ArgumentParser(description="A collection of tools useful for "
    + "exploration.")
subparsers = parser.add_subparsers(title="subcommands", help="sub-command help",
    dest="subCommand")

parser_bodycount = subparsers.add_parser("bodycount",
    help="Returns the number of bodies in a system. Will exit with code 1 on "
    + "server error and code 2 if the system could not be found in EDSM.")
parser_bodycount.add_argument("system", nargs=1)

parser_distance = subparsers.add_parser("distancebetween",
    help="Calculates the distance between two systems. Will exit with code 1 "
    + "on server error and code 2 if (one of) the systems could not be found "
    + "on EDSM.")
parser_distance.add_argument("system", nargs=2)

parser_find = subparsers.add_parser("findcommander",
    help="Attempts to find a CMDR’s last known position. Will exit with code 1 "
    + "on server error and code 2 if the CMDR could not be found on EDSM.")
parser_find.add_argument("name")
parser_find.add_argument("apikey", default="", nargs="?",
    help="the commander’s EDSM API key. Can be empty for public profiles.")

argcomplete.autocomplete(parser)
args = parser.parse_args()

# ===========================================================================

try:
  if args.subCommand == "bodycount":
    out = getBodyCount(args.system[0])
  elif args.subCommand == "distancebetween":
    out = distanceBetween(args.system[0], args.system[1])
  elif args.subCommand == "findcommander":
    out = findCommander(args.name, args.apikey)
except ServerError as e:
  print(e)
  sys.exit(1)
except NotFoundError as e:
  print(e)
  sys.exit(2)
else:
  print(out)
  sys.exit(0)
