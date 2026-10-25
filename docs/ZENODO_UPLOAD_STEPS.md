# Zenodo deposit steps

1. Log in to Zenodo.
2. Click `+` -> `New upload`.
3. Upload the prepared repository snapshot and the archival evidence/analysis files.
4. DOI:
   - answer `No` to "Do you already have a DOI for this upload?"
   - click `Get a DOI now!`.
5. Resource type: `Software`.
6. Copy the title, creator, description, and keywords from
   `metadata/ZENODO_FORM_VALUES.md`.
7. Licenses: add BOTH:
   - MIT License
   - Creative Commons Attribution 4.0 International (CC BY 4.0)
8. Set files to public/open.
9. Add the GitHub repository URL as a related identifier.
10. Click `Save draft`.
11. Do NOT publish yet.
12. Copy the reserved DOI into `CITATION.cff`, `README.md`, `codemeta.json`,
    and the manuscript reproducibility statement.
13. Build the DOI-bearing final release and replace the draft files if needed.
14. Preview and verify metadata/files/checksums.
15. Publish only after the DOI-bearing package and manuscript wording agree.
