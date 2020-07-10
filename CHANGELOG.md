# devel

## Added

* `spansh.py` old station snearch now takes a `--minage` (in days) argument for 
  what you would consider “outdated” data.

## Changed

* `spansh.py` old station search now outputs an age in days for the last update 
  instead of a time stamp.

# 0.5 (2020-07-01)

Changed Changelog format. Should be even clearer now at a glance!

See [KeepAChangelog](https://keepachangelog.com/en/1.0.0/).

## Added

* `edts.py`: Script for accessing Alot’s hosted EDTS API. Right now the only 
  implemented thing is getting approximate coordinates for a given procedually 
  generated system name.

# 0.4.1 (2020-06-18)

* removed accidentally left over debug print code from `spansh.py`

# 0.4 (2020-03-09)

Kind of a big one. Obviously because in addition to EDSM, I can now do some 
stuff with Spansh’s database. At this point I’m not sure if I want to keep it in 
the kind of hacky quick&dirty state it’s in right now or do another abstraction 
layer in addition to EDSM’s. Probably will be too lazy.

In addition to that the compiled version of the scripts for windows will now be 
a single executable file per script instead of having all the libraries stuff in 
subfolders. It’s cleaner that way, IMO.

## explorationtools.py

* `findcommander` now gives a last seen date for the position

known bugs:

* I need to fix the way the commander’s last seen is pulled. Right now searching 
  for a commander will error out if their profile is public, but their flight 
  logs (and thus the last updated time stamp) is not.

## spansh.py

* added `spansh.py` for accessing data from https://spansh.co.uk
* see the README for what it can do right now
