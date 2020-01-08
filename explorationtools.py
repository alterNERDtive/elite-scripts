#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse
import math
import sys

from pyEDSM.edsm.exception import ServerError, NotFoundError
from pyEDSM.edsm.models import System, Commander

# ===========================================================================

def getBodyCount(system):
  return System(system).bodyCount

def distanceBetween(system1, system2):
  systems = System.getSystems(system1, system2)
  return systems[0].distanceTo(systems[1])

def getCommanderPosition(name, apikey):
  coords = Commander(name, apikey).currentPosition
  ret = ""
  for k in coords:
    ret += "{}: {}, ".format(k, coords[k])
  return ret[:-2]

def getCommanderProfileUrl(name, apikey):
  return Commander(name, apikey).profileUrl

def getCommanderSystem(name, apikey):
  return Commander(name, apikey).currentSystem

def getSystemList(name):
  ret = ""

  systems = System.getSystems(name)
  for system in systems:
    ret += "{}\n".format(system.name)

  return ret[:-1]

# ===========================================================================

parser = argparse.ArgumentParser(description="A collection of tools useful for "
    + "exploration.")
subparsers = parser.add_subparsers(title="subcommands", help="sub-command help",
    dest="subCommand")

parser_bodycount = subparsers.add_parser("bodycount",
    help="Returns the number of bodies in a system. Will exit with code 1 on "
    + "server error and code 2 if the system could not be found in EDSM.")
parser_bodycount.add_argument("system", nargs=1, help="system to query")

parser_distance = subparsers.add_parser("distancebetween",
    help="Calculates the distance between two systems. Will exit with code 1 "
    + "on server error and code 2 if (one of) the systems could not be found "
    + "on EDSM.")
parser_distance.add_argument("system", nargs=2, help="the systems to measure")

parser_find = subparsers.add_parser("findcommander",
    help="Attempts to find a CMDR’s last known position. Will exit with code 1 "
    + "on server error and code 2 if the CMDR could not be found on EDSM.")
group = parser_find.add_mutually_exclusive_group(required=False)
group.add_argument('--system', action='store_true',
    help='output the commander’s last known system (default)')
group.add_argument('--coords', action='store_true',
    help='output the commander’s last known position in {x,y,z} coordinates')
group.add_argument('--url', action='store_true',
    help='output the commander’s profile URL')
parser_find.add_argument("name", help="the commander in question")
parser_find.add_argument("apikey", default="", nargs="?",
    help="the commander’s EDSM API key. Can be empty for public profiles.")

parser_bodycount = subparsers.add_parser("systemlist",
    help="Pulls all system names starting with the given string from EDSM")
parser_bodycount.add_argument("partialsystem", nargs=1,
    help="the partial system name to query against")

argcomplete.autocomplete(parser)
args = parser.parse_args()

# ===========================================================================

try:
  if args.subCommand == "bodycount":
    out = getBodyCount(args.system[0])
  elif args.subCommand == "distancebetween":
    out = distanceBetween(args.system[0], args.system[1])
  elif args.subCommand == "findcommander":
    if args.coords:
      out = getCommanderPosition(args.name, args.apikey)
    elif args.url:
      out = getCommanderProfileUrl(args.name, args.apikey)
    else:
      out = getCommanderSystem(args.name, args.apikey)
  elif args.subCommand == "systemlist":
    out = getSystemList(args.partialsystem)
except ServerError as e:
  print(e)
  sys.exit(1)
except NotFoundError as e:
  print(e)
  sys.exit(2)
else:
  print(out)
  sys.exit(0)
