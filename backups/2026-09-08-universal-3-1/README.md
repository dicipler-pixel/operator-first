# Original Universal 3.1 inputs

The three user uploads are preserved byte for byte: Compound_Eye_Universal_3_1_Complete.zip,
Compound_Eye_Universal_3_1.html, and Eye_Mixer_Guide.html. The ZIP is split into
ordered binary pieces so no repository file exceeds the connected upload request limit.
INPUTS.json records all original and part sizes and SHA-256 hashes.

From any directory, run:

```sh
python /path/to/restore_inputs.py --output /path/to/empty/folder
```

The standard-library-only script verifies every part and each reconstructed file.
The integrated current source is ../../tools/compound-eye/ . The earlier 2.0,
2.1 and 2.2 backups remain at ../2026-09-08/ . Original source preservation does
not endorse every historical scientific claim.
