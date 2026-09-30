# Scratch utilities (copied from the lead's scratchpad so they survive restarts)
- `acmoves.py`: official ac-r2-v1 moves on letter strings (x,X,y,Y), free reduction only; `run(R, path, show=True)` traces a path.
- `value.py FILE...`: values `id: [path]` lines against the latest boards in `research/acc/live/boards/` (run from the repo root).
- `lisitsa_find.py`: finds competition rows equal, up to relabelling/inversion/rotation/swap, to Lisitsa's
  MS_n(w*) = (X y^n x Y^(n+1), XYxyX); set `SAIR` to the SAIR checkout. 28 hits (14 AC + 14 SAC): the YXXyx chain.
