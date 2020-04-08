import os
import sys

from cx_Freeze import setup, Executable

from database import CURRENT_VERSION


executables = [Executable('rssim.py', targetName='rssim.exe', base='Win32GUI', icon='icon.ico')]

include_files = [
    ('db/patch', 'db/patch'), ('db/config.db', 'db/config.db'), ('db/default.db', 'db/default.db'), 'img', 'icon.ico',
    'font', 'shaders', 'resources.json'
]

excludes = [
    'PIL', 'test', 'email', 'html', 'http', 'urllib', 'dbm', 'pydoc_data', 'xml', 'xmlrpc', 'jdcal', 'et-xmlfile',
    'openpyxl', 'scipy', 'numpy.distutils', 'numpy.doc', 'numpy.f2py', 'numpy.fft', 'numpy.random', 'numpy.testing',
    'numpy.tests'
]

includes = [
    'pyglet', 'pyglet.app', 'pyglet.canvas', 'pyglet.clock', 'pyglet.extlibs', 'pyglet.font', 'pyglet.font.ttf',
    'pyglet.gl', 'pyglet.gl.glext_nv', 'pyglet.gl.glxext_nv', 'pyglet.gl.wglext_nv', 'pyglet.graphics',
    'pyglet.image', 'pyglet.image.codecs', 'pyglet.info', 'pyglet.input',
    'pyglet.libs', 'pyglet.libs.darwin', 'pyglet.libs.darwin.cocoapy', 'pyglet.libs.win32', 'pyglet.libs.x11',
    'pyglet.media', 'pyglet.media.drivers', 'pyglet.media.drivers.directsound',
    'pyglet.media.drivers.openal', 'pyglet.media.drivers.pulse', 'pyglet.resource', 'pyglet.sprite',
    'pyglet.text', 'pyglet.text.formats',
    'pyglet.window', 'pyglet.window.cocoa', 'pyglet.window.win32', 'pyglet.window.xlib',
    'keyring', 'keyring.__main__', 'keyring.backend', 'keyring.cli', 'keyring.core', 'keyring.credentials',
    'keyring.devpi_client', 'keyring.errors', 'keyring.http',
    'keyring.backends', 'keyring.backends._OS_X_API', 'keyring.backends.chainer', 'keyring.backends.fail',
    'keyring.backends.kwallet', 'keyring.backends.null', 'keyring.backends.OS_X',
    'keyring.backends.SecretService', 'keyring.backends.Windows', 'win32timezone',
    'controller', 'model', 'view', 'rssim_core', 'exceptions', 'i18n', 'notifications',
    'ui', 'database', 'ctypes', 'pycparser', 'libfuturize', 'libfuturize.fixes', 'multiprocessing',
    'past', 'past.translation', 'lib2to3', 'lib2to3.pgen2', 'ctypes', 'numpy.core'
]

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

setup(
    name='Railway Station Simulator',
    version='.'.join(str(v) for v in CURRENT_VERSION),
    description='Railway Station Simulator',
    executables=executables,
    options=options
)
