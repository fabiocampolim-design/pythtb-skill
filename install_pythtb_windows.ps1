# install_pythtb_windows.ps1
# Creates the conda environment and Jupyter kernel used by the PythTB notebooks.
# PythTB is pure Python, so (unlike Kwant) no compiled dependencies are needed.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File .\install_pythtb_windows.ps1
#   powershell -ExecutionPolicy Bypass -File .\install_pythtb_windows.ps1 -EnvName mytb -PythonVersion 3.13
#
# Parameters (all optional):
#   -EnvName        conda environment name            (default: pythtb)
#   -KernelName     Jupyter kernelspec name            (default: pythtb-mc — the notebooks are pinned to it)
#   -PythonVersion  Python version for the new env     (default: 3.12)
#   -SkipVerify     do not run verify_pythtb.py at the end
#
# Package versions come from requirements.txt (pythtb is pinned to 2.0.2 there).

param(
    [string]$EnvName = "pythtb",
    [string]$KernelName = "pythtb-mc",
    [string]$PythonVersion = "3.12",
    [switch]$SkipVerify
)

$ErrorActionPreference = "Stop"
$kernelDisplay = "Python $PythonVersion (miniconda - $EnvName)"
$req = Join-Path $PSScriptRoot "requirements.txt"

if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    throw "conda not found on PATH. Install Miniconda (https://docs.conda.io/en/latest/miniconda.html) first."
}
if (-not (Test-Path $req)) { throw "requirements.txt not found next to this script." }

Write-Host "== Creating conda env '$EnvName' (Python $PythonVersion) =="
conda create -n $EnvName python=$PythonVersion -y

Write-Host "== Installing PythTB and the scientific stack from requirements.txt =="
conda run -n $EnvName python -m pip install -r $req

Write-Host "== Registering Jupyter kernel '$KernelName' ('$kernelDisplay') =="
conda run -n $EnvName python -m ipykernel install --user --name $KernelName --display-name $kernelDisplay

if (-not $SkipVerify) {
    Write-Host "== Verifying =="
    conda run -n $EnvName python (Join-Path $PSScriptRoot "scripts\verify_pythtb.py")
}

Write-Host "Done. Open chapters\PythTB_00_Introduction.ipynb (index: chapters\README.md) with kernel '$kernelDisplay'."
Write-Host "Regression suite: conda run -n $EnvName python -m pytest tests"
