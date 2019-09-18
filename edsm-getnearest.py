#!/usr/bin/env python3
import argparse
import math
import requests
import sys
import tkinter as tk

from pyEDSM.edsm.exception import ServerError, NotFoundError
from pyEDSM.edsm.models import System, Commander

class EdsmApiException(Exception):
  pass


# =================================================================================

def getCmdrCoords (cmdr):
  resp = requests.get('https://www.edsm.net/api-logs-v1/get-position?commanderName={}&showCoordinates=1'.format(cmdr))
  if resp.status_code != 200:
    raise EdsmApiException('GET /get-position/ {}'.format(resp.status_code))
  try:
    ret = resp.json()['coordinates']
  except KeyError:
    raise EdsmApiException('Coordinates for CMDR {} not found!'.format(cmdr))
  return ret

def distance (coords1, coords2):
  return math.sqrt( (coords1['x']-coords2['x'])**2
      + (coords1['y']-coords2['y'])**2
      + (coords1['z']-coords2['z'])**2 )

def getDistances (system, cmdrs):
  systemcoords = System(system).coords
  distances = {}
  for cmdr in cmdrs:
    cmdrcoords = getCmdrCoords(cmdr)
    distances[cmdr] = round(distance(cmdrcoords, systemcoords))
  return distances

# =================================================================================

def outputGui():
  def runsearch(event=None):
    for child in frame.winfo_children():
      child.grid_remove()
      child.destroy()
    try:
      distances = getDistances(systemField.get(), cmdrs)
      nearestCmdr = min(distances,key=distances.get)
      lbl = tk.Label(
          frame, text='nearest CMDR: {} ({} ly from {})'.format(nearestCmdr,
            distances[nearestCmdr], system))
      lbl.grid(row=0, columnspan=2)
      row = 1
      for cmdr in distances:
        row += 1
        lbl = tk.Label(frame, text='{}:'.format(cmdr))
        lbl.grid(row=row, column=0)
        lbl = tk.Label(frame, text='{} ly'.format(distances[cmdr]))
        lbl.grid(row=row, column=1)
    except (ServerError, NotFoundError) as e:
      lbl = tk.Label(frame, text=e)
      lbl.grid(row=0, columnspan=2)
  window = tk.Tk()
  window.title('EDSM nearest CMDR')
  lbl = tk.Label(window, text='system:')
  lbl.grid(row=0, column=0)
  systemField = tk.Entry(window, width=50)
  systemField.grid(row=0, column=1)
  systemField.insert(tk.END, system)
  systemField.focus()
  frame = tk.Frame(window)
  frame.grid(row=1, columnspan=3)
  btn = tk.Button(window, text='get distances', command=runsearch)
  btn.grid(row=0, column=2)
  window.bind('<Return>', runsearch)
  window.attributes('-topmost', True)
  runsearch()
  window.mainloop()

# =================================================================================

def outputText():
  try:
    distances = getDistances(system, cmdrs)
  except (ServerError, NotFoundError) as e:
    print(e)
    exit(1)
  nearestCmdr = min(distances,key=distances.get)
  if shortOutput:
    print('nearest commander: {} ({} ly).'.format(nearestCmdr,
      distances[nearestCmdr]))
  else:
    print('nearest CMDR: {} ({} ly from {}).'.format(nearestCmdr,
      distances[nearestCmdr], system))
    print()
    for cmdr in distances:
      print('{}: {} ly'.format(cmdr, distances[cmdr]))

# =================================================================================

parser = argparse.ArgumentParser(description='Locate your CMDRs using EDSM and '
    + 'find their distance to a given system.')
parser.add_argument('cmdrs', metavar='CMDR', nargs='+', help='a list of CMDR names '
    + '(must have their location public on EDSM!)')
parser.add_argument('--system', nargs=1, help='the target system (must be in '
    + 'EDDN!)', required=True)
parser.add_argument('--short', action='store_true', help='short output (only '
    + 'makes sense with `--text`)')
group = parser.add_mutually_exclusive_group()
group.add_argument('--gui', action='store_true', help='explicitly run the GUI')
group.add_argument('--text', action='store_true', help='explicitly give text output')

args = parser.parse_args()

system = args.system[0].strip().replace(' ', '').replace('', '')
cmdrs = args.cmdrs
shortOutput = args.short

# =================================================================================

if args.text:
  outputText()
elif args.gui:
  outputGui()
else:
  try:
    outputGui()
  except tk.TclError:
    outputText()
