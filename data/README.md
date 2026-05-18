# Data

Provenance and access for the data behind this paper.

For each dataset, record:

- **What it is** — model outputs, prompts, transcripts, human codes.
- **How it was collected** — script, date range, model versions/endpoints.
- **Where it lives** — committed here if small and non-sensitive; otherwise the
  external location and how to obtain it.
- **Schema** — columns/fields and their meaning.

`data/raw/` and `data/cache/` are git-ignored by default (see `.gitignore`).
Commit only small, derived, shareable data. Large or sensitive raw data is
described here, not committed — replication uses the collection script.
