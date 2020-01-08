# A collection of useful scripts around Elite Dangerous #

## Requirements ##

* argcomplete
* argparse
* requests
* Tkinter

You probably want to install your distribution/OS package for Tkinter instead of
using pip. Then do the good old `pip install --user -r requirements.txt` or
`pip3 install --user -r requirements.txt`.

## edsm-getnearest.py ##

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

## explorationtools.py ##

```
usage: explorationtools.py [-h] {bodycount,distancebetween,findcommander} ...

A collection of tools useful for exploration.

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {bodycount,distancebetween,findcommander}
                        sub-command help
    bodycount           Returns the number of bodies in a system. Will exit
                        with code 1 on server error and code 2 if the system
                        could not be found in EDSM.
    distancebetween     Calculates the distance between two systems. Will exit
                        with code 1 on server error and code 2 if (one of) the
                        systems could not be found on EDSM.
    findcommander       Attempts to find a CMDR’s last known position. Will
                        exit with code 1 on server error and code 2 if the
                        CMDR could not be found on EDSM.
```

```
usage: explorationtools.py bodycount [-h] system

positional arguments:
  system      system to query

optional arguments:
  -h, --help  show this help message and exit
```

```
usage: explorationtools.py distancebetween [-h] system system

positional arguments:
  system      the systems to measure

optional arguments:
  -h, --help  show this help message and exit
```

```
usage: explorationtools.py findcommander [-h] [--system | --url] name [apikey]

positional arguments:
  name        the commander in question
  apikey      the commander’s EDSM API key. Can be empty for public profiles.

optional arguments:
  -h, --help  show this help message and exit
  --system    output the commander’s last known system (default)
  --url       output the commander’s profile URL
```

## Need Help / Want to Contribute? ##

Just [file an issue](https://github.com/alterNERDtive/elite-scripts/issues/new)
here or [hop into Discord](https://discord.gg/uUKFdW) if that is your thing.
