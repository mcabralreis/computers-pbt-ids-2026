# GitHub Upload Steps (Windows / PowerShell)

The prepared repository ZIP is intentionally small (~1.3 MB) and excludes the 314 MB final evidence archive.

## 1. Unpack

```powershell
Expand-Archive .\Computers_PBT_IDS_REPOSITORY_R1.zip -DestinationPath .\repo_unpack
cd .\repo_unpack\Computers_PBT_IDS_REPRODUCIBILITY_R1
```

## 2. Review the license decision

Before making the repository public, replace `LICENSE_SELECTION_REQUIRED.md` with the chosen license file(s) and update `CITATION.cff` if the selected license is to be declared there.

## 3. Initialize Git

```powershell
git init
git add .
git commit -m "Initial reproducibility release v1.0.0"
git branch -M main
```

## 4. Connect the empty public repository you create on GitHub

```powershell
git remote add origin https://github.com/<USER_OR_ORG>/<REPOSITORY>.git
git push -u origin main
```

## 5. Tag the release

```powershell
git tag -a v1.0.0 -m "Reproducibility package v1.0.0"
git push origin v1.0.0
```

Then create the corresponding GitHub Release `v1.0.0`.

## Important

Do not add `R7_D35_PF4_PRIMARY_P1_A1_G3_R3_FINAL_COMPLETE_evidence.zip` to normal Git history. It is >100 MiB and belongs in the DOI-bearing archival upload set.
