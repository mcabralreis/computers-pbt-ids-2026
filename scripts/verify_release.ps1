param(
    [string]$ArchiveDir = ""
)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Py = "py"
$Args = @("$Root\scripts\verify_release.py")
if ($ArchiveDir -ne "") {
    $Args += @("--archive-dir", $ArchiveDir)
}
& $Py @Args
if ($LASTEXITCODE -ne 0) { throw "Release verification failed." }
