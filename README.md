# idgaf - test GTK packaging

This is a tiny test project to verify packaging a GTK Python app and producing a .deb package.

## Project layout and purpose

Top-level files and folders

- `meson.build` — Meson project file (original upstream build definition). Not required by the simplified Debian packaging we use in this repo, but left for upstream builds.
- `idgaf/` — the Python package containing the application code:
  - `__init__.py`, `__main__.py`, `app.py` — application entry points and logic.
- `scripts/` — helper launcher scripts installed to `/usr/bin` by the package:
  - `idgaf` — launcher that runs `python3 -m idgaf` (installed as `/usr/bin/idgaf`).
- `data/` — application data shipped with the package:
  - `idgaf.desktop` — desktop entry for application menus.
  - `icons/hicolor/48x48/apps/idgaf.svg` — application icon (hicolor theme path).
- `debian/` — Debian packaging metadata and install instructions:
  - `control` — package metadata and Build-Depends.
  - `changelog` — Debian changelog (version information).
  - `rules` — debhelper makefile, controls build/install hooks.
  - `install` — maps files from the source tree into package locations.
  - other generated files may appear here after building; they can be safely ignored or removed.
- `.gitignore` — ignores build artifacts, python cache, and debian generated files.

## Commands — step by step

### Prerequisites (install once on your system)

You need Debian packaging tools and Python. On Debian/Ubuntu:

```bash
sudo apt update
sudo apt install -y build-essential debhelper-compat dh-python python3-all python3-gi
```

If you want to build via Meson (upstream):

```bash
sudo apt install -y meson ninja-build
```

### 1) Setup project (clone / prepare)

If you haven't already cloned the repo:

```bash
git clone <repo-url> mydir && cd mydir
# or if already in repo root
cd /home/ashu/Code/linux/fuck_deploy
```

Install a virtualenv to test locally (optional but recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pygobject
```

### 2) Build

Option A — Debian binary package (recommended for installable .deb):

```bash
# build a binary .deb using debhelper (this repo ships packaging metadata)
cd /home/ashu/Code/linux/fuck_deploy
dpkg-buildpackage -b -us -uc
# resulting .deb will be in the parent directory (/home/ashu/Code/linux)
```

Option B — Meson upstream build (if you want upstream artifacts)

```bash
meson setup builddir
meson compile -C builddir
meson install -C builddir --destdir=$PWD/_install
```

### 3) Install

Install the produced .deb (binary package):

```bash
sudo dpkg -i /home/ashu/Code/linux/idgaf_0.1.0_all.deb
sudo apt-get install -f   # fix any missing dependencies
```

After install, the following items are available system-wide:
- `/usr/bin/idgaf` — launcher executable
- `/usr/lib/python3/dist-packages/idgaf` — Python package
- `/usr/share/applications/idgaf.desktop` — desktop entry (application menu)
- `/usr/share/icons/hicolor/48x48/apps/idgaf.svg` — icon

### 4) Test

Run the app from terminal:

```bash
idgaf
# or
python3 -m idgaf
```

Verify the desktop file and icon (optional):

```bash
desktop-file-validate /usr/share/applications/idgaf.desktop
ls -l /usr/share/icons/hicolor/48x48/apps/idgaf.*
```

### 5) Uninstall

Remove the package and installed files:

```bash
sudo dpkg -r idgaf
# or to purge configuration files too:
sudo dpkg -P idgaf
```

### 6) Cleanup

Remove build artifacts and generated debian files from the working tree:

```bash
cd /home/ashu/Code/linux/fuck_deploy
debian/rules clean
rm -rf builddir _install obj-* idgaf_deb
rm -f ../idgaf_*.deb ../idgaf_*.changes ../idgaf_*.buildinfo
# Optional: remove generated debian staging directory
rm -rf debian/idgaf debian/.debhelper debian/*.debhelper debian/*.substvars debian/*.log debian/files debian/debhelper-build-stamp
```

## Notes and tips

- If you plan to produce official Debian packages or source uploads, prefer using Meson and a proper Build-Depends like `python3-meson` in `debian/control` and build in a clean chroot (`sbuild` / `pbuilder`).
- For local development, using the virtualenv and `python3 -m idgaf` is simplest.
- Keep the files in `debian/` that you edit (control, changelog, rules, install) and ignore/remove the generated files committed by debhelper.

## FAQ, common errors & troubleshooting

<details>
<summary><strong>dpkg-buildpackage fails with "Tried to use unknown language 'python'" or Meson errors</strong></summary>

Reason: Meson can't find the Python language plugin (meson-python). Your `debian/control` originally referenced Meson; either install the plugin or use the simplified dh_python3 flow.

Quick fixes:

- For local testing, install meson-python in a dedicated environment:

```bash
python3 -m venv .venv && . .venv/bin/activate && pip install meson meson-python
```

- Or use the packaged workflow in this repo (we removed meson from Build-Depends); run:

```bash
dpkg-buildpackage -b -us -uc
```

</details>

<details>
<summary><strong>The application doesn't appear in my desktop menu after install</strong></summary>

Make sure the desktop file and icon were installed and caches updated:

```bash
ls -l /usr/share/applications/idgaf.desktop
ls -l /usr/share/icons/hicolor/48x48/apps/idgaf.*
sudo update-desktop-database
sudo gtk-update-icon-cache /usr/share/icons/hicolor || true
```

Log out and back in if your desktop environment still doesn't show it.

</details>

<details>
<summary><strong>Running `idgaf` says "command not found"</strong></summary>

Confirm `/usr/bin/idgaf` exists (installed by the package). If not, reinstall the .deb or run the app via:

```bash
python3 -m idgaf
```

</details>

<details>
<summary><strong>"Unable to locate package meson-python" when trying to `apt install` it</strong></summary>

Many distributions don't ship a package named exactly `meson-python`. Prefer installing `meson` (available) and the meson-python plugin from PyPI in a virtualenv for local builds, or add `python3-meson` to Build-Depends if your distro provides that.

</details>

<details>
<summary><strong>dpkg-deb warns about owner/group when building manually</strong></summary>

That's because building as your user produces files owned by your UID; use:

```bash
dpkg-deb --build --root-owner-group <dir> <output.deb>
```

or let `dpkg-buildpackage` handle ownership for you.

</details>

<details>
<summary><strong>Tips</strong></summary>

- Keep generated `debian/` files out of version control. Use the provided `.gitignore` and run `debian/rules clean` after builds.
- For reproducible builds or publishing, use a clean chroot (`sbuild`/`pbuilder`) and proper Build-Depends. For local convenience, the simplified flow is fine.
- If packaging grows, consider adding simple tests that run `python3 -m idgaf --version` or headless checks to CI.

</details>

Still stuck? Paste the failing lines from `dpkg-buildpackage` or `meson` output and I can help debug further.
