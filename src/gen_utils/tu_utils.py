
def checkResult(expected, function, args):
    if function(*args) != expected:
        print(f"{function.__name__} should return {expected} with args {args}, it returned {function(*args)}")
        assert(False)

def checkResultSilent(expected, function, args):
    if function(*args) != expected:
        print(f"{function.name} didn't return expected results with args {args}")
        assert(False)
        