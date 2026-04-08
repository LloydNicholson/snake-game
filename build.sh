#!/bin/bash
set -e

cd "$(dirname "$0")"

# Create venv and install dependencies if missing
if [ ! -x venv/bin/python ]; then
    echo "Setting up build environment..."
    python3 -m venv venv
fi

if ! ./venv/bin/python - <<'PY' >/dev/null 2>&1
import pygame.mixer
PY
then
    echo "Installing audio-enabled pygame..."
    ./venv/bin/pip install --quiet --upgrade --force-reinstall pygame-ce
fi

if [ ! -f venv/bin/pyinstaller ]; then
    ./venv/bin/pip install --quiet --upgrade pyinstaller
fi

echo "Cleaning old build..."
rm -rf dist build/*/ __pycache__

echo "Rebuilding snake game..."
./venv/bin/pyinstaller --clean --distpath dist -y snake_game.spec

echo "Build complete! Run ./dist/snake_game"
