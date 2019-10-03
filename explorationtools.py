#!/usr/bin/env python3
import argparse
import math
import sys

from pyEDSM.edsm.exception import ServerError, NotFoundError
from pyEDSM.edsm.models import System, Commander

# ===========================================================================

def getBodyCount(system):
  try:
    bodyCount = System(system).bodyCount
  except ServerError as e:
    print(e)
    sys.exit(1)
  except NotFoundError as e:
    print(e)
    sys.exit(2)
  else:
    print(bodyCount)
    sys.exit(0)

# ===========================================================================

parser = argparse.ArgumentParser(description="A collection of tools useful for "
    + "exploration.")
subparsers = parser.add_subparsers(title="subcommands", help="sub-command help",
    dest="subCommand")

parser_bodycount = subparsers.add_parser("bodycount",
    help="Returns the number of bodies in a system. Will exit with code 1 on "
    + "server error and code 2 if the system could not be found in EDSM.")
parser_bodycount.add_argument("system", nargs=1, help="the system in question")

args = parser.parse_args()

# ===========================================================================

if args.subCommand == "bodycount":
  getBodyCount(args.system[0])
