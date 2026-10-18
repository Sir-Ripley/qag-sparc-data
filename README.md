# QAG SPARC Data — live dataset for the Kinetics Lab explorer

Public JSON dataset backing the "Explore all 175 galaxies" section of the
QAG Kinetics Lab (https://qag-kinetics-lab.vercel.app/).

**Live endpoint:** `https://qag-sparc-data.vercel.app/galaxies175.json`
(CORS `*`, cache 1h)

## Files

| File | Description |
|---|---|
| `galaxies175.json` | **Deployed file.** Slim web derivative (see `build.py`). Served by this Vercel project. |
| `galaxies175.full.json` | **Source of truth.** Full fidelity: all 175 galaxies, all 3,391 SPARC points at full precision, per-galaxy fits, provenance + schema docs embedded. |
| `build.py` | Regenerates the slim file from the full file. Run after any data update. |
| `ingest_manifest.json` | Ingestion provenance (per-file SHA1, source archive hash). |
| `vercel.json` | CORS + cache headers for the JSON endpoint. |

## Data provenance

- **Source:** SPARC database (Lelli, McGaugh & Schombert 2016), `Rotmod_LTG.zip`
  (SHA1 `ab2c19f22bf51b26abbba3083b6a45e31a970488`) — repo `.dat` files verified byte-identical.
- **Ingestion:** `ingest_sparc.py` v1.0.0, 2026-10-18 (Sir-Ripley/QAGKinetics `code/`).
- **Fits:** `sweep_v3.py`, 2026-10-18 — per-galaxy least squares on
  v²(r) = Υ★(v_disk²+v_bulge²) + v_gas² + v_∞²(1−e^(−r/r_aff)), Υ★ = 0.5 fixed.
- **Results:** QAG reduced χ² 5.55 (median 1.42) vs MOND 56.55 vs Newton 616.74;
  QAG wins 167/175 vs MOND, 170/175 vs Newton; ΔBIC = 172,054.
- **Flags:** `low_dof` = only 4 data points (D512-2, NGC6789, UGC00634, UGC07232);
  `pinned` = r_aff hit the 60 kpc boundary (rising outer curves).

## Schema (full file)

`galaxies.<NAME>` → `{v_inf, r_aff, qag_red, mond_red, newt_red, qag_rms, low_dof, pinned, pts}`
`pts` → `[[r_kpc, vobs_kms, err_kms, v_baryon_kms], …]`
with `v_baryon = √(0.5·(v_disk² + v_bulge²) + v_gas²)`.

## Updating

1. Re-run the sweep in QAGKinetics (`code/sweep_v3.py`).
2. Replace `galaxies175.full.json` (+ update provenance block).
3. Run `python3 build.py`.
4. Push — Vercel auto-deploys (git-connected).
