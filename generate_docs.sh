#!/usr/bin/env bash
cat > README.md << EOF
# A collection of useful scripts around Elite Dangerous #

## Requirements ##

* argcomplete
* argparse
* requests
* Tkinter

You probably want to install your distribution/OS package for Tkinter instead of
using pip. Then do the good old \`pip install --user -r requirements.txt\`.

You’ll also need to install pyEDSM’s dependencies:
\`pip install --user -r pyEDSM/requirements.txt\`

## Pre-Compiled Version (Windows) ##

If you check the
[releases](https://github.com/alterNERDtive/elite-scripts/releases) you’ll find
a .zip file with pre-compiled scripts that don’t need Python installed. Mostly
a) for saving myself some hassle and b) because that’s easier to distribute with
my
[VoiceAttack profiles](https://github.com/alterNERDtive/VoiceAttack-profiles).

## Scripts ##

### edsm-getnearest.py ###

\`\`\`
EOF
./edsm-getnearest.py -h >> README.md
cat >> README.md << EOF
\`\`\`

### edts.py ###

\`\`\`
EOF
./edts.py -h >> README.md
cat >> README.md << EOF
\`\`\`

\`\`\`
EOF
./edts.py coords -h >> README.md
cat >> README.md << EOF
\`\`\`

### explorationtools.py ###

\`\`\`
EOF
./explorationtools.py -h >> README.md
cat >> README.md << EOF
\`\`\`

\`\`\`
EOF
./explorationtools.py bodycount -h >> README.md
cat >> README.md << EOF
\`\`\`

\`\`\`
EOF
./explorationtools.py distancebetween -h >> README.md
cat >> README.md << EOF
\`\`\`

\`\`\`
EOF
./explorationtools.py findcommander -h >> README.md
cat >> README.md << EOF
\`\`\`

\`\`\`
EOF
./explorationtools.py findsystem -h >> README.md
cat >> README.md << EOF
\`\`\`

\`\`\`
EOF
./explorationtools.py systemlist -h >> README.md
cat >> README.md << EOF
\`\`\`

### spansh.py ###

\`\`\`
EOF
./spansh.py -h >> README.md
cat >> README.md << EOF
\`\`\`

\`\`\`
EOF
./spansh.py nearestsystem -h >> README.md
cat >> README.md << EOF
\`\`\`

\`\`\`
EOF
./spansh.py oldstations -h >> README.md
cat >> README.md << EOF
\`\`\`

\`\`\`
EOF
./spansh.py systemexists -h >> README.md
cat >> README.md << EOF
\`\`\`

## Need Help / Want to Contribute? ##

Just [file an issue](https://github.com/alterNERDtive/elite-scripts/issues/new)
here or [hop into Discord](https://discord.gg/XHNX7jN) if that is your thing.
EOF
