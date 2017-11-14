where /q python
IF ERRORLEVEL 1 (
    ECHO Python is required!
    set /p DUMMY=press any key to quit
) ELSE (
    python src/make_all.py %1
)