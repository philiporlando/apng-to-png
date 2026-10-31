# APNG Frame Extractor

[![CI](https://github.com/philiporlando/apng-to-png/actions/workflows/ci.yml/badge.svg)](https://github.com/philiporlando/apng-to-png/actions/workflows/ci.yml)

Extract every frame of an animated PNG (APNG) into individual PNG files. The script processes all `.apng` files in a folder at once, and each animation gets its own output folder.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Usage

Put your APNG files in `data/input/`, then run the script from the repository root:

```bash
mkdir -p data/input
cp path/to/*.apng data/input/
uv run python -m apng_to_png.apng_to_png
```

uv installs the dependencies on the first run. Frames are written to `data/output/<file name>/`, numbered from zero:

```
data/
├── input/
│   ├── spinner.apng
│   └── wave.apng
└── output/
    ├── spinner/
    │   ├── frame_000.png
    │   ├── frame_001.png
    │   └── ...
    └── wave/
        └── ...
```

Frame numbers are zero-padded to at least three digits, so the files sort in order.

### Things to know

- **Only files ending in `.apng` are processed** (in any letter case). Many APNGs use a `.png` extension; rename them to `.apng` first.
- **`data/input/` must exist.** If it's missing, the script exits with an error. `data/output/` is created automatically.
- **Existing frames are overwritten** when you re-run the script on the same file.
- **Frames are extracted as stored, not composited.** Optimized APNGs often store only the region that changed from the previous frame. In that case, frames after the first may be smaller partial images rather than full snapshots of the animation.
- **One bad file doesn't stop the run.** If a file fails to parse, the error is logged and the script moves on to the next file.

`data/` is gitignored, so your input and output files stay out of version control.

## Development

```bash
uv sync            # install runtime and dev dependencies
uv run pytest      # run the test suite
```

CI runs the tests on every push to `main` and on every pull request. Dependabot opens weekly PRs for dependency and GitHub Actions updates.
