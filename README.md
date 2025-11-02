idgaf - test GTK packaging

This is a tiny test project to verify packaging a GTK Python app and producing a .deb package.

Project layout and purpose
--------------------------

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

Commands — step by step
-----------------------

Prerequisites (install once on your system)

You need Debian packaging tools and Python. On Debian/Ubuntu:

```bash
sudo apt update
sudo apt install -y build-essential debhelper-compat dh-python python3-all python3-gi
```

If you want to build via Meson (upstream):

```bash
sudo apt install -y meson ninja-build
```

1) Setup project (clone / prepare)

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

2) Build

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

3) Install

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

4) Test

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

5) Uninstall

Remove the package and installed files:

```bash
sudo dpkg -r idgaf
# or to purge configuration files too:
sudo dpkg -P idgaf
```

6) Cleanup

Remove build artifacts and generated debian files from the working tree:

```bash
cd /home/ashu/Code/linux/fuck_deploy
debian/rules clean
rm -rf builddir _install obj-* idgaf_deb
rm -f ../idgaf_*.deb ../idgaf_*.changes ../idgaf_*.buildinfo
# Optional: remove generated debian staging directory
rm -rf debian/idgaf debian/.debhelper debian/*.debhelper debian/*.substvars debian/files debian/debhelper-build-stamp
```

Notes and tips
--------------
- If you plan to produce official Debian packages or source uploads, prefer using Meson and a proper Build-Depends like `python3-meson` in `debian/control` and build in a clean chroot (`sbuild` / `pbuilder`).
- For local development, using the virtualenv and `python3 -m idgaf` is simplest.
- Keep the files in `debian/` that you edit (control, changelog, rules, install) and ignore/remove the generated files committed by debhelper.

If you want, I can add more details (CI steps, linting, packaging checklist) or make the README shorter.
