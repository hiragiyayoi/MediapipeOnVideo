
@echo off
rem This script was created by Nuitka to execute 'main.exe' with Python DLL being found.
set PATH=c:\program files\python312;%PATH%
set PYTHONHOME=C:\Program Files\Python312
set NUITKA_PYTHONPATH=.;C:\Program Files\Python312\DLLs;C:\Program Files\Python312\Lib;C:\Program Files\Python312;.;.\Lib\site-packages
"%~dp0main.exe" %*
