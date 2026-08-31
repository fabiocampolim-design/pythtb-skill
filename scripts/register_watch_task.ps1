# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
<#
.SYNOPSIS  Register (or -Remove) a weekly Windows Task Scheduler job that runs
           watch_upstream.py --weekly --pull (playbook S8 / rule 23).
.PARAMETER Python   interpreter (default %USERPROFILE%\miniconda3\envs\pythtb\python.exe)
.PARAMETER Day      weekday of the trigger (default Monday)
.PARAMETER At       time of the trigger, HH:mm (default 08:00)
.PARAMETER Remove   unregister the task instead
.PARAMETER DryRun   print what would be registered, register nothing
.PARAMETER Version  print the pythtb-skill version
Exit 0 ok, 1 failed.
#>
param(
    [string]$Python = "$env:USERPROFILE\miniconda3\envs\pythtb\python.exe",
    [string]$Day = "Monday",
    [string]$At = "08:00",
    [switch]$Remove,
    [switch]$DryRun,
    [switch]$Version
)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($Version) { Write-Output ("pythtb-skill " + (Get-Content (Join-Path $here "..\VERSION") -Raw).Trim()); exit 0 }
$script = Join-Path $here "watch_upstream.py"
$name = "pythtb-skill upstream watch"
$argument = "`"$script`" --weekly --pull -q"
if ($DryRun) {
    Write-Output "DRY-RUN: Register-ScheduledTask '$name' weekly $Day $At -> `"$Python`" $argument"
    exit 0
}
if ($Remove) {
    Unregister-ScheduledTask -TaskName $name -Confirm:$false
    Write-Output "removed '$name'"
    exit 0
}
if (-not (Test-Path $Python)) { Write-Output "python not found: $Python"; exit 1 }
$action = New-ScheduledTaskAction -Execute $Python -Argument $argument -WorkingDirectory $here
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $Day -At $At
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 1)
Register-ScheduledTask -TaskName $name -Action $action -Trigger $trigger -Settings $settings `
    -Description "pythtb-skill S8 weekly upstream watch (GitHub releases/issues/PRs + PyPI + clone pull)" -Force | Out-Null
Write-Output "registered '$name' weekly $Day $At -> $Python"
