"""Python wrapper around environment modules ("module load")
"""
import os
import sys
from subprocess import run, PIPE

__version__ = '0.1'

_cached_pythonpath = os.getenv('PYTHONPATH', '')
_auto_fix_sys_path = 0

def _modulecmd(*args):
    cmd = ['modulecmd', 'python'] + list(args)
    res = run(cmd, stdout=PIPE, stderr=PIPE)
    txt = res.stderr.decode('utf-8', 'replace').strip()
    if txt:
        print(txt)

    res.check_returncode()
    
    code = res.stdout.decode('utf-8').strip()
    if code:
        exec(code, {'os': os})

    if _auto_fix_sys_path:
        fix_sys_path()

def load(*args):
    _modulecmd('load', *args)

def unload(*args):
    _modulecmd('unload', *args)

def set_auto_fix_sys_path(new):
    global _auto_fix_sys_path
    _auto_fix_sys_path = bool(new)

def get_auto_fix_sys_path():
    return _auto_fix_sys_path

def fix_sys_path():
    global _cached_pythonpath
    pypath = os.getenv('PYTHONPATH', '')
    if pypath == _cached_pythonpath:
        # Nothing to do if PYTHONPATH has not changed
        return

    # PYTHONPATH has changed, see what changed
    oldpypaths = _cached_pythonpath.split(':')
    newpypaths = pypath.split(':')

    oldpyset = set(oldpypaths)
    newpyset = set(newpypaths)

    oldpyonly = []
    newpyonly = []

    # Find elements only in oldpypaths
    for path in oldpypaths:
        if path not in newpyset:
            oldpyonly.append(path)

    # Find elements only in newpypaths
    # We reverse the order for this list (prepend instead of append)
    for path in newpypaths:
        if path not in oldpyset:
            newpyonly.insert(0, path)

    # Modify sys.path
    # Remove from sys.path paths in oldpypaths only
    for path in oldpyonly:
        sys.path.remove(path)

    # Prepend to sys.path paths in newpypaths only
    for path in newpyonly:
        sys.path.insert(0, path)

    # Cache the new PYTHONPATH
    _cached_pythonpath = pypath


