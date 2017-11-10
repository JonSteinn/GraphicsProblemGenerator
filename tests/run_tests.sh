#!/bin/bash

python -m unittest discover -s ${PWD} -t ${PWD}
read -p "Press any key to quit"