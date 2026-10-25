# Deposit Guide — GitHub + Zenodo

## Recommended publication pattern

1. Publish the lightweight repository contents on GitHub (or an equivalent source-code host).
2. Create a tagged release, e.g. `v1.0.0`.
3. Archive the release and large evidence files in Zenodo.
4. Use the **version-specific DOI** in the manuscript for exact reproducibility. Keep the Zenodo Concept DOI for the evolving project record.
5. Insert the final DOI/repository URL into the manuscript only after the record has actually been created.

Zenodo issues a DOI for each published version and a separate Concept DOI representing all versions. For reproducibility, cite the version-specific DOI.

## Why the PF4 evidence ZIP should not be committed to GitHub history

The final PF4 evidence archive is approximately 314 MB. GitHub blocks regular Git objects above 100 MiB. Keep this file out of Git history and upload it to the archival record instead.

## Suggested Zenodo upload set

Upload the files listed in `evidence/EXPECTED_ARCHIVAL_FILES.md`. The prepared upload set contains fewer than 100 files and is far below Zenodo's current 50 GB per-record quota.

## DOI strategy

If you want the DOI printed inside files before publication, Zenodo supports reserving a DOI for a manual deposit. For the GitHub integration workflow, Zenodo documentation states that a DOI cannot be pre-reserved before the GitHub release; use a manual upload if pre-reservation is needed.

## Metadata

Use `metadata/DEPOSIT_METADATA_DRAFT.md` and `CITATION.cff` as the starting point. Add the final license choice and DOI before publication.
