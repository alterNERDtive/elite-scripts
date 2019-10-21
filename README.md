# A collection of useful scripts around Elite Dangerous #

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
usage: explorationtools.py [-h] {bodycount,distancebetween} ...

A collection of tools useful for exploration.

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {bodycount,distancebetween}
                        sub-command help
    bodycount           Returns the number of bodies in a system. Will exit
                        with code 1 on server error and code 2 if the system
                        could not be found in EDSM.
	distancebetween     Calculates the distance between two systems. Will exit
                        with code 1 on server error and code 2 if (one of) the
						systems could not be found on EDSM.
```

```
usage: explorationtools.py bodycount [-h] system

positional arguments:
  system

optional arguments:
  -h, --help  show this help message and exit
```

```
usage: explorationtools.py distancebetween [-h] system system

positional arguments:
  system

optional arguments:
  -h, --help  show this help message and exit
```
