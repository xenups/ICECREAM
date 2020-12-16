def make_project():
    import os
    import sys
    project_root = os.path.abspath(os.curdir)
    root_name, _, _ = __name__.partition('.')
    root_module = sys.modules[root_name]
    ice_cream_root = os.path.dirname(root_module.__file__)
    assets_address = ice_cream_root + os.sep + 'assets' + os.sep + 'project_assets.zip'

    import zipfile
    with zipfile.ZipFile(assets_address, 'r') as zip_ref:
        zip_ref.extractall(project_root)
