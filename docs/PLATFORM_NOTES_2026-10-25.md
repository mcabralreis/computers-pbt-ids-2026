# Platform Notes — verified 2026-10-25

These limits can change; re-check provider documentation immediately before deposit.

## GitHub

- regular Git objects larger than 100 MiB are blocked;
- files larger than 50 MiB trigger a warning;
- generated/binary large evidence should be stored outside ordinary Git history or via an archival service/Git LFS;
- the prepared repository snapshot is far below these limits.

## Zenodo

- current per-record quota: up to 50 GB;
- current maximum: 100 files per record;
- the prepared upload set is ~338 MB and fewer than 100 files;
- published records receive a version DOI and a Concept DOI;
- manual deposits can reserve a DOI before publication;
- Zenodo's GitHub integration does not support pre-reserving a DOI before the GitHub release.
