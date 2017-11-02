import ctypes as C


eh_fn = C.CFUNCTYPE(None, C.c_char_p, C.c_void_p)

class ErrorHandler(C.Structure):
    _fields_ = [
        ("eh", eh_fn),
        ("user_data", C.c_void_p)
    ]
