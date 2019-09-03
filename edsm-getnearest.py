#!/usr/bin/env python3
import math
import requests
import sys
import tkinter as tk

from tkinter import messagebox

if len(sys.argv) < 3:
    exit(1)

class EdsmApiException(Exception):
    pass

def getSystemCoords (system):
    resp = requests.get('https://www.edsm.net/api-v1/system?systemName={}&showCoordinates=1'.format(system))
    if resp.status_code != 200:
        raise EdsmApiException('GET /system/ {}'.format(resp.status_code))
    try:
        ret = resp.json()['coords']
    except TypeError:
        raise EdsmApiException('System coordinates for {} not found!'.format(system))
    return ret

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
    systemcoords = getSystemCoords(system)
    distances = {}
    for cmdr in cmdrs:
        cmdrcoords = getCmdrCoords(cmdr)
        distances[cmdr] = round(distance(cmdrcoords, systemcoords))
    return distances

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
        except EdsmApiException as e:
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
    window.geometry('450x200+550+-650')
    window.bind('<Return>', runsearch)
    window.attributes('-topmost', True)
    window.mainloop()

def outputText():
    try:
        distances = getDistances(system, cmdrs)
    except EdsmApiException as e:
        print(e)
        exit(1)
    nearestCmdr = min(distances,key=distances.get)
    print('nearest CMDR: {} ({} ly from {})'.format(nearestCmdr, 
        distances[nearestCmdr], system))
    print()
    for cmdr in distances:
        print('{}: {} ly'.format(cmdr, distances[cmdr]))

sys.argv.pop(0) # script name
system = sys.argv.pop(0)
cmdrs = sys.argv

outputGui()
# try:
    # outputGui()
# except tk.TclError:
    # outputText()
