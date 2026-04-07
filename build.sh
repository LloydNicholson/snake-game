#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "Cleaning old build..."
rm -rf dist build/*/ __pycache__ venv/lib/*/pygame/*.pyc venv/lib/python3.*/*.pyc

echo "Rebuilding snake game..."
./venv/bin/pyinstaller --clean --distpath dist -y snake_game.spec

echo "Build complete! Run ./dist/snake_game"