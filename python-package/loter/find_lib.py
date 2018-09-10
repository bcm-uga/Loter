import ctypes as C
import os
import sys
import pkg_resources
from glob import glob

class LoterLibraryNotFound(Exception):
    """Error thrown when loter is not found"""
    pass

def _get_lib():
    # dirpath = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
    # libpath_possible = [os.path.join(dirpath, '../../lib/', 'libloter.so'),
    #                     os.path.join(dirpath, '../', 'libloter.so')]
    # libpath = [path for path in libpath_possible if os.path.exists(path) and os.path.isfile(path)]
    # if not libpath:
    #     raise LoterLibraryNotFound("Library not found in :\n" + '\n'.join(libpath_possible))

    libpath = glob(pkg_resources.resource_filename('loter',
                   os.path.join('_loter_wrap*.so')))

    if not libpath:
        for dir in sys.path:
            libpath = glob(os.path.join(dir, 'loter', '_loter_wrap*.so'))
            if libpath:
                break
        if not libpath:
            raise LoterLibraryNotFound("Library `_loter_wrap.so` not found")

    selected_lib = libpath[0]
    lib = C.cdll.LoadLibrary(selected_lib)

    return lib

_LIB = _get_lib()
