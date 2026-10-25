# GitHub finalization - v1.0.0

Repository: https://github.com/mcabralreis/computers-pbt-ids-2026

The repository already exists. Update it with the DOI-bearing files from `Computers_PBT_IDS_REPOSITORY_v1.0.0.zip`. In particular, replace `CITATION.cff`, `README.md`, `metadata/codemeta.json`, `docs/DATA_AVAILABILITY.md`, and release metadata.

After the DOI-bearing content is committed:

1. Verify the main branch shows DOI `10.5281/zenodo.23640914` and repository URL correctly.
2. Run `py .\scripts\verify_release.py` from a local clone/extracted release.
3. Create tag/release `v1.0.0`.
4. Use release title: `v1.0.0 - Reproducibility release`.
5. Do not upload the ~314 MB final evidence ZIP to ordinary Git history; it belongs in Zenodo.
