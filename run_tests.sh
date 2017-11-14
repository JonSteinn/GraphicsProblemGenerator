#!/bin/bash

cd tests
python -m unittest discover -s "${PWD}" -t "${PWD}"
cd ..
read -p "Press any key to quit"