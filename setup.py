import os
import sys

from cx_Freeze import setup, Executable


executables = [Executable('rssim.py',
                          targetName='rssim.exe',
                          base='Win32GUI',
                          icon='icon.ico')]

include_files = [('db/patch', 'db/patch'), ('db/config.db', 'db/config.db'), ('db/default.db', 'db/default.db'),
                 'img', 'icon.ico', 'font', 'shaders']

excludes = ['PIL', 'test', 'distutils', 'email', 'html', 'http', 'unittest', 'urllib', 'dbm', 'pydoc_data',
            'xml', 'xmlrpc']

includes = ['pyglet',
            'pyglet.app',
            'pyglet.canvas',
            'pyglet.clock',
            'pyglet.extlibs',
            'pyglet.font', 'pyglet.font.ttf',
            'pyglet.gl', 'pyglet.gl.glext_nv', 'pyglet.gl.glxext_nv', 'pyglet.gl.wglext_nv',
            'pyglet.graphics',
            'pyglet.image', 'pyglet.image.codecs',
            'pyglet.info',
            'pyglet.input',
            'pyglet.libs', 'pyglet.libs.darwin', 'pyglet.libs.darwin.cocoapy', 'pyglet.libs.win32', 'pyglet.libs.x11',
            'pyglet.media', 'pyglet.media.drivers', 'pyglet.media.drivers.directsound',
            'pyglet.media.drivers.openal', 'pyglet.media.drivers.pulse', 'pyglet.media.sources',
            'pyglet.resource',
            'pyglet.sprite',
            'pyglet.text', 'pyglet.text.formats',
            'pyglet.window', 'pyglet.window.carbon', 'pyglet.window.cocoa', 'pyglet.window.win32', 'pyglet.window.xlib',
            'ctrl', 'model', 'view', 'car_skins_collection', 'rssimcore']

options = {
    'build_exe': {
        'include_msvcr': True,
        'includes': includes,
        'excludes': excludes,
        'include_files': include_files
    }
}

os.environ['TCL_LIBRARY'] = r'{}\tcl\tcl8.6'.format(sys.exec_prefix)
os.environ['TK_LIBRARY'] = r'{}\tcl\tk8.6'.format(sys.exec_prefix)

setup(name='Railway Station Simulator',
      version='0.9.2',
      description='Railway Station Simulator',
      executables=executables,
      options=options)
