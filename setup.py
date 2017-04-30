from py2exe.build_exe import py2exe
from distutils.core import setup
import sys
import shutil

sys.argv.append('py2exe')

setup(
    options = {
        'py2exe': {
            'optimize': 2,
            'bundle_files': 2,
            'compressed': True,
            'dll_excludes': ['w9xpopen.exe'],
        }
    },
    zipfile = None,
    console = [{
    'script': 'app.py',
    'copyright': 'Copyright (C) 2017 orygin10',
    'company_name': 'orygin10',
    'icon_resources': [(0, "favicon.ico")]
    }],

    version = '0.1',
    name = 'pyt411',
    description = 'T411 Interface'
)

shutil.rmtree('build/')
