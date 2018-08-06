from cx_Freeze import setup, Executable

executables = [Executable('rssim.py')]

include_files = ['img', 'base_route_cfg']

options = {
    'build_exe': {
        'include_msvcr': True,
        'include_files': include_files
    }
}

setup(name='Railway Station Simulator',
      version='0.0.1',
      description='first_prototype',
      executables=executables,
      options=options)