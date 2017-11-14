#!/bin/sh

hash python 2>/dev/null || { echo >&2 "Python is required!"; read -p "Press any key to quit"; }
python src/make_all.py "$@"