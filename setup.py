from cx_Freeze import setup, Executable

executables = [Executable('rssim.py')]

include_files = ['img', 'cfg']

options = {
    'build_exe': {
        'include_msvcr': True,
        'include_files': include_files
    }
}

setup(name='Railway Station Simulator',
      version='0.0.1',
      description='Railway Station Simulator',
      executables=executables,
      options=options)
