project('idgaf', 'python',
  version: '0.1.0',
  meson_version: '>= 0.59.0'
)

python = import('python')
py = python.find_installation('python3')

# install python package
python_dir = join_paths(get_option('prefix'), py.get_install_dir())
install_subdir('idgaf', install_dir: python_dir)

# install launcher and desktop
install_data('scripts/idgaf-launcher', install_dir: get_option('bindir'), install_mode: 'rwxr-xr-x', rename: 'idgaf')
install_data('data/idgaf.desktop', install_dir: get_option('datadir') / 'applications')
