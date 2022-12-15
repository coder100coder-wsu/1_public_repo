from install_pkgs import import_or_install

def setup_packages(counter=0, bool_var=False, required_pkgs={}):
    for pkg in required_pkgs:
        import_or_install(pkg)
    return 1

# run once to setup required packages in virtual_env
# setup_packages(bool_var=True)
