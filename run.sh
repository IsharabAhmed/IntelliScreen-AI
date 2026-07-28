#!/usr/bin/env bash
if [ -d "venv" ]; then
    ./venv/bin/python run.py "$@"
else
    python3 run.py "$@"
fi
