where /q python
IF ERRORLEVEL 1 (
    ECHO Python is required!    
    set /p DUMMY=press any key to quit
) ELSE (
    cd tests
    python -m unittest discover -s "%cd%" -t "%cd%"
    cd ..
    set /p DUMMY=press any key to quit
)