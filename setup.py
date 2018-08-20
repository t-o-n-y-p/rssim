from cx_Freeze import setup, Executable

executables = [Executable('rssim.py',
                          targetName='rssim.exe',
                          base='Win32GUI',
                          icon='icon.ico')]

include_files = ['img', 'default_cfg', 'logs_config.ini', 'game_config.ini']

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
