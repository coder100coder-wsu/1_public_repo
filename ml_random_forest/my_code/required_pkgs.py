# file contains names of packages required
def required_packages(bool_start=False):
    required_pkgs = {'pandas',
                     'numpy',
                     'scikit-learn',
                     'statsmodels',
                     'Path',
                     'os'}
    if bool_start:
        return required_pkgs
