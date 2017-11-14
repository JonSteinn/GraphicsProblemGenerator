#!/bin/bash

hash python 2>/dev/null || { echo >&2 "Python is required!"; read -p "Press any key to quit"; }
cd tests
python -m unittest discover -s "${PWD}" -t "${PWD}"
cd ..
read -p "Press any key to quit"