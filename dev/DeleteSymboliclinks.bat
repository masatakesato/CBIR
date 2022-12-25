@echo off
cd /d %~dp0

if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)


set target=".\preprocess\preprocess"
if exist %target% (
    echo removing existing symboliclink... %target%
    rmdir %target%
)


set target=".\apps\apps"
if exist %target% (
    echo removing existing symboliclink... %target%
    rmdir %target%
)