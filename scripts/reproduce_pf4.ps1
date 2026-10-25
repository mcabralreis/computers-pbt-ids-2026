param(
    [Parameter(Mandatory=$true)][string]$EvidenceZip,
    [string]$OutDir = ".\reproduced_pf4"
)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
py "$Root\analysis\reproduce_pf4_results.py" --evidence-zip "$EvidenceZip" --outdir "$OutDir"
if ($LASTEXITCODE -ne 0) { throw "PF4 reproduction failed." }
py "$Root\analysis\validate_reproduction.py" --reproduced "$OutDir"
if ($LASTEXITCODE -ne 0) { throw "PF4 validation failed." }
