# Analysis

Code that turns `data/` into `results/`.

- `scripts/` — analysis scripts. Each script states at the top: what it
  reads (data/), what it writes (results/), and how to run it.

## Convention

Every figure or number in the paper traces back to exactly one script here.
Name results after the script that produced them so the chain is obvious:
`scripts/clamping_by_version.py` → `results/clamping_by_version.csv` +
`results/clamping_by_version.pdf`.

Reproducibility: pin dependencies (`requirements.txt` or equivalent) and make
scripts deterministic where possible (fixed seeds, recorded model versions).
