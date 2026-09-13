# Zenodo Deposit Checklist

For each archive:

1. Upload exactly the named ZIP from `RELEASE_INDEX.md`.
2. Copy the corresponding `.zenodo.json` metadata from inside the archive.
3. Preserve the version number and author spelling `Jeromie N. Beasley`.
4. Add the resulting DOI to the release README and GitHub release notes only after Zenodo assigns it.
5. Do not reuse an older DOI unless the deposit is explicitly created as a new version of that exact record.
6. Verify the uploaded file's SHA-256 against `RELEASE_INDEX.md` before publishing.
7. Keep every scope fence visible in the Zenodo description.

Recommended deposit order: Elemental Foundations Revision 4, Atlas finite kernels, Collatz exact finite interfaces, Yang–Mills finite operator kernels, then the optional umbrella archive.
