def compose(*functions):
    def inner(arg):
        for f in reversed(functions):
            arg = f(*arg)
        return arg
    return inner

def repeated(function, n):
    def r_function(arg):
        for _ in xrange(n):
            arg = function(arg)
        return arg
    return r_function
