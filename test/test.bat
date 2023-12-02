@echo off

set "EXE_FOLDER=D:\Work\Program\Course\Programming practices\Final work\test\input"
set "PYTHON_SCRIPT=D:\Work\Program\Course\Programming practices\Final work\scripts\main.py"
set "OUTPUT_FOLDER=D:\Work\Program\Course\Programming practices\Final work\test\output"

echo Starting script...

for %%i in ("%EXE_FOLDER%\*.txt") do (
    echo Processing file: %%i
    type "%%i" | python "%PYTHON_SCRIPT%" >> "%OUTPUT_FOLDER%\output_%%~ni.txt"
)

echo All files processed.
pause