#!/usr/bin/env bash
cat > README.md << EOF
# A collection of useful scripts around Elite Dangerous #

## Requirements ##

* argcomplete
* argparse
* requests
* Tkinter

You probably want to install your distribution/OS package for Tkinter instead of
using pip. Then do the good old \`pip install --user -r requirements.txt\` or
\`pip3 install --user -r requirements.txt\`.

## edsm-getnearest.py ##

\`\`\`
EOF
./edsm-getnearest.py -h >> README.md
cat >> README.md << EOF
\`\`\`

## explorationtools.py ##

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

## Need Help / Want to Contribute? ##

Just [file an issue](https://github.com/alterNERDtive/elite-scripts/issues/new)
here or [hop into Discord](https://discord.gg/uUKFdW) if that is your thing.
EOF
