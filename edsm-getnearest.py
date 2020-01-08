#!/usr/bin/env python3
import argparse
import math
import requests
import sys
import tkinter as tk

from pyEDSM.edsm.exception import CommanderNotFoundError, ServerError, SystemNotFoundError
from pyEDSM.edsm.models import Commander, System

# =================================================================================

def getDistances (system, cmdrs, roundTo=2):
  distances = {}
  for cmdr in cmdrs:
    distances[cmdr] = system.distanceTo(cmdr, roundTo=roundTo)
  return distances

# =================================================================================

def outputGui():
  def runsearch(event=None):
    for child in frame.winfo_children():
      child.grid_remove()
      child.destroy()
    try:
      system = System(systemField.get())
      distances = getDistances(system, cmdrs)
      nearestCmdr = min(distances,key=distances.get)
      lbl = tk.Label(
          frame, text='nearest CMDR: {} ({} ly from {})'.format(nearestCmdr.name,
            distances[nearestCmdr], system.name))
      lbl.grid(row=0, columnspan=2)
      row = 1
      for cmdr in distances:
        row += 1
        lbl = tk.Label(frame, text='{}:'.format(cmdr.name))
        lbl.grid(row=row, column=0)
        lbl = tk.Label(frame, text='{} ly'.format(distances[cmdr]))
        lbl.grid(row=row, column=1)
    except (ServerError, SystemNotFoundError) as e:
      lbl = tk.Label(frame, text=e)
      lbl.grid(row=0, columnspan=2)
    except EdsmApiException as e:
      lbl = tk.Label(frame, text=e)
      lbl.grid(row=0, columnspan=2)
  window = tk.Tk()
  window.title('EDSM nearest CMDR')
  lbl = tk.Label(window, text='system:')
  lbl.grid(row=0, column=0)
  systemField = tk.Entry(window, width=50)
  systemField.grid(row=0, column=1)
  systemField.insert(tk.END, system.name)
  systemField.focus()
  frame = tk.Frame(window)
  frame.grid(row=1, columnspan=3)
  btn = tk.Button(window, text='get distances', command=runsearch)
  btn.grid(row=0, column=2)
  window.bind('<Return>', runsearch)
  runsearch()
  window.mainloop()

# =================================================================================

def outputText():
  if shortOutput:
    roundTo=0
  else:
    roundTo=2
  try:
    distances = getDistances(system, cmdrs, roundTo=roundTo)
  except CommanderNotFoundError as e:
    print(e)
    sys.exit(1)
  except ServerError as e:
    print(e)
    sys.exit(1)
  except SystemNotFoundError as e:
    print(e)
    sys.exit(2)
  except EdsmApiException as e:
    print(e)
    sys.exit(1)
  nearestCmdr = min(distances,key=distances.get)
  if shortOutput:
    print('nearest commander: {} ({} ly).'.format(nearestCmdr.name,
      int(distances[nearestCmdr])))
  else:
    print('nearest CMDR: {} ({} ly from {}).'.format(nearestCmdr.name,
      distances[nearestCmdr], system.name))
    print()
    for cmdr in distances:
      print('{}: {} ly'.format(cmdr.name, distances[cmdr]))
    sys.exit(0)

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

system = System(args.system[0].strip().replace(' ', '').replace('', ''))
cmdrs = []
for name in args.cmdrs:
  cmdrs += [Commander(name)]
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
