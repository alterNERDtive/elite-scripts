# A collection of useful scripts around Elite Dangerous #

## Requirements ##

* argcomplete
* argparse
* requests
* Tkinter

You probably want to install your distribution/OS package for Tkinter instead of
using pip. Then do the good old `pip install --user -r requirements.txt`.

You’ll also need to install pyEDSM’s dependencies:
`pip install --user -r pyEDSM/requirements.txt`

## Pre-Compiled Version (Windows) ##

If you check the
[releases](https://github.com/alterNERDtive/elite-scripts/releases) you’ll find
a .zip file with pre-compiled scripts that don’t need Python installed. Mostly
a) for saving myself some hassle and b) because that’s easier to distribute with
my
[VoiceAttack profiles](https://github.com/alterNERDtive/VoiceAttack-profiles).

## Scripts ##

### edsm-getnearest.py ###

```
usage: edsm-getnearest.py [-h] --system SYSTEM [--short] [--gui | --text]
                          CMDR [CMDR ...]

Locate your CMDRs using EDSM and find their distance to a given system.

positional arguments:
  CMDR             a list of CMDR names (must have their location public on
                   EDSM!)

optional arguments:
  -h, --help       show this help message and exit
  --system SYSTEM  the target system (must be in EDDN!)
  --short          short output (only makes sense with `--text`)
  --gui            explicitly run the GUI
  --text           explicitly give text output
```

### explorationtools.py ###

```
usage: explorationtools.py [-h]
                           {bodycount,distancebetween,findcommander,findsystem,systemlist}
                           ...

A collection of tools useful for exploration.

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {bodycount,distancebetween,findcommander,findsystem,systemlist}
                        sub-command help
    bodycount           Returns the number of bodies in a system. Will exit
                        with code 1 on server error and code 2 if the system
                        could not be found in EDSM.
    distancebetween     Calculates the distance between two systems. Will exit
                        with code 1 on server error and code 2 if (one of) the
                        systems could not be found on EDSM.
    findcommander       Attempts to find a CMDR’s last known position. Will
                        exit with code 1 on server error and code 2 if the
                        CMDR could not be found on EDSM. Will also give you
                        the time of last activity if you search for their
                        system.
    findsystem          Attempts to find a partially matching system that
                        should then hopefully be in the vicinity of the given
                        system
    systemlist          Pulls all system names starting with the given string
                        from EDSM
```

```
usage: explorationtools.py bodycount [-h] system

positional arguments:
  system      system to query

optional arguments:
  -h, --help  show this help message and exit
```

```
usage: explorationtools.py distancebetween [-h] [--roundto [ROUNDTO]]
                                           system system

positional arguments:
  system               the systems to measure

optional arguments:
  -h, --help           show this help message and exit
  --roundto [ROUNDTO]  the number of digits to round to (default: 2)
```

```
usage: explorationtools.py findcommander [-h] [--system | --coords | --url]
                                         name [apikey]

positional arguments:
  name        the commander in question
  apikey      the commander’s EDSM API key. Can be empty for public profiles.

optional arguments:
  -h, --help  show this help message and exit
  --system    output the commander’s last known system (default)
  --coords    output the commander’s last known position in {x,y,z}
              coordinates
  --url       output the commander’s profile URL
```

```
usage: explorationtools.py findsystem [-h] system

positional arguments:
  system      the system in question

optional arguments:
  -h, --help  show this help message and exit
```

```
usage: explorationtools.py systemlist [-h] partialsystem

positional arguments:
  partialsystem  the partial system name to query against

optional arguments:
  -h, --help     show this help message and exit
```

### spansh.py ###

```
usage: spansh.py [-h] {nearestsystem,oldstations} ...

Script for interfacing with Spansh’s API.

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {nearestsystem,oldstations}
                        sub-command help
    nearestsystem       Searches for the nearest system in the database to
                        given coordinates.
    oldstations         Searches for stations with old data (>1 year without
                        an update.
```

```
usage: spansh.py nearestsystem [-h] [--short] coordinate coordinate coordinate

positional arguments:
  coordinate  the coordinates to search for (order: x, y, z)

optional arguments:
  -h, --help  show this help message and exit
  --short     short output format (system name only)
```

```
usage: spansh.py oldstations [-h] [--system [SYSTEM]] [--count [COUNT]]
                             [--short]

optional arguments:
  -h, --help         show this help message and exit
  --system [SYSTEM]  a single system to query. If not present, get the oldest
                     stations overall.
  --count [COUNT]    how many stations to output. Defaults to 50.
  --short            short output format (system/station names only)
```

## Need Help / Want to Contribute? ##

Just [file an issue](https://github.com/alterNERDtive/elite-scripts/issues/new)
here or [hop into Discord](https://discord.gg/uUKFdW) if that is your thing.
