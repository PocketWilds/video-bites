from distutils.core import setup
import py2exe

packages = []

setup(windows=['main.py'],
    data_files=[],
    options={'py2exe':{'bundle_files': 1}}
    
)