@echo off
cd /d "%~dp0"
where uv >nul 2>nul
if errorlevel 1 (
  echo Install uv first ^(see README.md^), reopen your terminal, and try again.
  pause
  exit /b 1
)
set "task_uv_group="
for %%a in (%*) do if "%%~a"=="d2-1" set "task_uv_group=--group prompting"
for %%a in (%*) do if "%%~a"=="d2-2" set "task_uv_group=--group rag"
uv run --locked %task_uv_group% python start.py %*
if errorlevel 1 pause
