#!/usr/bin/env bash
cat > README.md << EOF
# A collection of useful scripts around Elite Dangerous #

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
./explorationtools.py findCommander -h >> README.md
cat >> README.md << EOF
\`\`\`
EOF
