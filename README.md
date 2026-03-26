# Collection of Blender Addons for Molecular Structures

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10776696.svg)](https://doi.org/10.5281/zenodo.10776696)
[![Lint](https://github.com/Tonner-Zech-Group/blender-importASE/actions/workflows/lint.yml/badge.svg)](https://github.com/Tonner-Zech-Group/blender-importASE/actions/workflows/lint.yml)
[![Unit tests](https://github.com/Tonner-Zech-Group/blender-importASE/actions/workflows/test-unit.yml/badge.svg)](https://github.com/Tonner-Zech-Group/blender-importASE/actions/workflows/test-unit.yml)
[![Blender tests](https://github.com/Tonner-Zech-Group/blender-importASE/actions/workflows/test-blender.yml/badge.svg)](https://github.com/Tonner-Zech-Group/blender-importASE/actions/workflows/test-blender.yml)

## Supported Blender versions

| Addon version | Blender | Branch |
|---|---|---|
| 2.x (current) | 4.4.x, 4.5.x LTS | `main` |

## Dependencies

ASE (Atomic Simulation Environment) is automatically installed on first activation via `pip`. An internet connection is required for automatic installation.

### Manual dependency installation

If no internet connection is available:

1. Open the Blender scripting panel and run: `bpy.utils.script_path_user() + "/modules"` to find the modules directory
2. Install ASE manually: `pip install ase --target <install_dir>`
3. Restart Blender

## Installation

Download `blender_importASE.zip` from the [latest release](https://github.com/Tonner-Zech-Group/blender-importASE/releases). In Blender: **Edit → Preferences → Addons → Install**, select the zip, then activate the addon. To also install the viewport rendering addon, repeat with `render_vpts.py`.

## Usage

Import molecules via **File → Import** and use **Render → Render VPTs** to render all collections separately for each camera in your scene.

Name cameras descriptively (`top`, `side`, `front`) — `camera.001` won't help you find the output images.

---

## Development

### Prerequisites

- Python 3.11+
- Blender 4.4+ (see [multi-version setup](#blender-versions) below)
- Git

### Quick start

```bash
git clone git@github.com:Tonner-Zech-Group/blender-importASE.git
cd blender-importASE
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### Blender versions

Multiple Blender versions are managed under `/opt/blender/`. Use the provided script to set up the runner or your local machine:

```bash
sudo bash scripts/setup_runner.sh
```

This installs Blender 4.4.3 and 4.5.8-lts under `/opt/blender/` and places a version-switching wrapper at `/usr/local/bin/blender`.

The active version is controlled by a `.blender-version` file in the repository root:

```
4.4.3
```

### Development install (symlink)

Symlink the addon directly into Blender's addons directory so edits take effect on the next **F3 → Reload Scripts**:

```bash
ln -s "$PWD/blender_importASE" ~/.config/blender/4.4/scripts/addons/blender_importASE
ln -s "$PWD/blender_importASE" ~/.config/blender/4.5/scripts/addons/blender_importASE
```

### Running tests

**Pure Python tests** (no Blender required):

```bash
pytest test/ -k "TestFunctions" -v
```

**Full test suite** (requires Blender in PATH):

```bash
pytest test/ -v
```

**With coverage:**

```bash
pytest test/ -v --cov --cov-report=term
```

### Code style

Ruff is enforced in CI on every push and pull request:

```bash
ruff check .          # check
ruff check --fix .    # auto-fix safe issues
```

### Contributing

- Target branch for new features and fixes: `main`
- One feature or fix per commit; each commit must pass `ruff check` and `pytest test/ -k TestFunctions`
- Backports to `blender/x.y-lts` maintenance branches are done by cherry-pick PR

### CI

| Workflow | Runner | Triggers |
|---|---|---|
| `lint.yml` | ubuntu-latest | all pushes and PRs |
| `test-unit.yml` | ubuntu-latest | all pushes and PRs |
| `test-blender.yml` | self-hosted Linux | pushes/PRs to `main` and `autotest`; manual dispatch |

The Blender workflow runs a matrix over Blender 4.4.3 and 4.5.8-lts. To set up a self-hosted runner, see [`scripts/setup_runner.sh`](scripts/setup_runner.sh).
