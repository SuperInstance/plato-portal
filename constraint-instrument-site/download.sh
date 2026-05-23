#!/usr/bin/env bash
# Constraint Instrument — One-command setup
# Works on Linux and macOS
# Usage: bash <(curl -sL https://superinstance.github.io/constraint-instrument-site/download.sh)

set -e

RED='\033[0;31m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
DIM='\033[0;2m'
BOLD='\033[1m'
RESET='\033[0m'

echo ""
echo -e "${CYAN}${BOLD}🎵 The Constraint Instrument${RESET}"
echo -e "${DIM}Bathymetrics for Music${RESET}"
echo ""

# Check Python
if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    echo -e "${RED}Error: Python 3.10+ is required.${RESET}"
    echo "Install it from https://python.org or your package manager."
    exit 1
fi

PYVER=$($PY -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "  Python: ${GREEN}${PYVER}${RESET} ✓"

# Check git
if ! command -v git &>/dev/null; then
    echo -e "${RED}Error: git is required.${RESET}"
    exit 1
fi
echo -e "  git:    ${GREEN}$(git --version | awk '{print $3}')${RESET} ✓"
echo ""

# Install directory
INSTALL_DIR="${HOME}/constraint-instrument"
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${DIM}Updating existing installation...${RESET}"
    cd "$INSTALL_DIR"
    git pull --rebase 2>/dev/null || true
else
    echo -e "${CYAN}Cloning constraint-synth...${RESET}"
    git clone https://github.com/SuperInstance/constraint-synth "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Install
echo -e "${CYAN}Installing...${RESET}"
$PY -m pip install -e . --quiet 2>/dev/null || $PY -m pip install -e .

echo ""
echo -e "${GREEN}${BOLD}✓ Installed!${RESET}"
echo ""

# Run demo if the demo script exists
if [ -f "demo_30sec.py" ]; then
    echo -e "${CYAN}Running 30-second demo...${RESET}"
    echo ""
    $PY demo_30sec.py || true
    echo ""
fi

echo -e "${CYAN}${BOLD}Quick start:${RESET}"
echo ""
echo -e "  ${DIM}\$${RESET} ${BOLD}cd${RESET} ${INSTALL_DIR}"
echo -e "  ${DIM}\$${RESET} ${BOLD}${PY}${RESET} examples/demo_synth.py"
echo ""
echo -e "  ${DIM}# Or in Python:${RESET}"
echo -e "  ${DIM}\$${RESET} ${BOLD}${PY}${RESET} -c \"from constraint_synth import ConstraintSynth; \\
    s = ConstraintSynth.from_preset('blues_guitar'); \\
    signal = s.play_note(64, 90, 0.5); \\
    ConstraintSynth.to_wav(signal, 'note.wav'); \\
    print('🎵 note.wav written')\""
echo ""
echo -e "${DIM}Docs: https://github.com/SuperInstance/constraint-synth${RESET}"
echo -e "${DIM}Playground: open constraint-instrument-site/playground.html${RESET}"
echo ""
