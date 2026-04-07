#!/bin/bash
set -e

cd "$(dirname "$0")"

# Create venv and install dependencies if missing
if [ ! -f venv/bin/pyinstaller ]; then
    echo "Setting up build environment..."
    python3 -m venv venv
    ./venv/bin/pip install --quiet pygame pyinstaller
fi

echo "Cleaning old build..."
rm -rf dist build/*/ __pycache__

echo "Rebuilding snake game..."
./venv/bin/pyinstaller --clean --distpath dist -y snake_game.spec

echo "Build complete! Run ./dist/snake_game"