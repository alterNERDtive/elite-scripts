#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse
import math
import sys
from datetime import datetime

from pyEDSM.edsm.exception import ServerError, NotFoundError
from pyEDSM.edsm.models import System, Commander

# ===========================================================================

def getBodyCount(system):
  return System(system).bodyCount

def distanceBetween(system1, system2, roundTo=2):
  systems = System.getSystems(system1, system2)
  distance = systems[0].distanceTo(systems[1], roundTo)
  if roundTo == 0:
    distance = int(distance)
  return distance

def getCommanderPosition(name, apikey):
  coords = Commander(name, apikey).currentPosition
  ret = "hidden"
  if coords:
    ret = ""
    for k in coords:
      ret += "{}: {}, ".format(k, coords[k])
    ret = ret[:-2]
  return ret

def getCommanderProfileUrl(name, apikey):
  return Commander(name, apikey).profileUrl

def getCommanderSystem(name, apikey):
  cmdr = Commander(name, apikey)
  if cmdr.lastActivity is None:
    return "{}".format(cmdr.currentSystem)
  else:
    return "{} (last seen {})".format(cmdr.currentSystem,
        when(cmdr.lastActivity))
def when(date):
  diff = datetime.now() - date
  ret = ""
  if diff.days > 0:
    ret += "{} days ".format(diff.days)
  if diff.seconds > 0:
    hours = int(diff.seconds / 3600)
    if hours > 0:
      ret += "{} hours ".format(hours)
    minutes = int(diff.seconds % 3600 / 60)
    if minutes > 0:
      ret += "{} minutes ".format(minutes)
    if diff.days == 0 and hours == 0 and minutes == 0:
      # ONLY seconds!
      ret = "{} seconds ".format(diff.seconds)
  ret += "ago"
  return ret

def getSystemList(name):
  systems = System.getSystems(name)
  ret = ""
  for system in systems:
    ret += "{}\n".format(system.name)
  return ret[:-1]

def getSystemNear(name):
  # Probably want to abort at _some_ point. I’m defining two full words left as
  # the condition for that now.
  if name.count(' ') < 2:
    ret = "Aborting search at {}, require more than 2 words to limit the "
    ret += "result set."
    return ret.format(name)

  try:
    systems = System.getSystems(name)
  except NotFoundError:
    return getSystemNear(name[:-1])
  else:
    ret = ""
    for system in systems:
      ret += "{} ({}, {}, {})\n".format(system.name,
          system.coords['x'], system.coords['y'], system.coords['z'])
    return ret[:-1]

# ===========================================================================

parser = argparse.ArgumentParser(description="A collection of tools useful for "
    + "exploration.")
subparsers = parser.add_subparsers(title="subcommands", help="sub-command help",
    dest="subcommand", required=True)

parser_bodycount = subparsers.add_parser("bodycount",
    help="Returns the number of bodies in a system. Will exit with code 1 on "
    + "server error and code 2 if the system could not be found in EDSM.")
parser_bodycount.add_argument("system", nargs=1, help="system to query")

parser_distance = subparsers.add_parser("distancebetween",
    help="Calculates the distance between two systems. Will exit with code 1 "
    + "on server error and code 2 if (one of) the systems could not be found "
    + "on EDSM.")
parser_distance.add_argument("--roundto", nargs="?", type=int, default=2,
    help="the number of digits to round to (default: 2)")
parser_distance.add_argument("system", nargs=2, help="the systems to measure")

parser_findCmdr = subparsers.add_parser("findcommander",
    help="Attempts to find a CMDR’s last known position. Will exit with code 1 "
    + "on server error and code 2 if the CMDR could not be found on EDSM. Will "
    + "also give you the time of last activity if you search for their system.")
group = parser_findCmdr.add_mutually_exclusive_group(required=False)
group.add_argument('--system', action='store_true',
    help='output the commander’s last known system (default)')
group.add_argument('--coords', action='store_true',
    help='output the commander’s last known position in {x,y,z} coordinates')
group.add_argument('--url', action='store_true',
    help='output the commander’s profile URL')
parser_findCmdr.add_argument("name", help="the commander in question")
parser_findCmdr.add_argument("apikey", default="", nargs="?",
    help="the commander’s EDSM API key. Can be empty for public profiles.")

parser_findSystem = subparsers.add_parser("findsystem",
    help="Attempts to find a partially matching system that should then "
    + "hopefully be in the vicinity of the given system")
parser_findSystem.add_argument("system", help="the system in question")

parser_bodycount = subparsers.add_parser("systemlist",
    help="Pulls all system names starting with the given string from EDSM")
parser_bodycount.add_argument("partialsystem", nargs=1,
    help="the partial system name to query against")

argcomplete.autocomplete(parser)
args = parser.parse_args()

# ===========================================================================

try:
  if args.subcommand == "bodycount":
    out = getBodyCount(args.system[0])
  elif args.subcommand == "distancebetween":
    out = distanceBetween(args.system[0], args.system[1], args.roundto)
  elif args.subcommand == "findcommander":
    if args.coords:
      out = getCommanderPosition(args.name, args.apikey)
    elif args.url:
      out = getCommanderProfileUrl(args.name, args.apikey)
    else:
      out = getCommanderSystem(args.name, args.apikey)
  elif args.subcommand == "findsystem":
    out = getSystemNear(args.system)
  elif args.subcommand == "systemlist":
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
