cd tests
python -m unittest discover -s "%cd%" -t "%cd%"
cd ..
set /p DUMMY=press any key to quit