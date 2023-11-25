def stringToBool(val):
    if len(val) == 1:
        if val == "阴":
            val = True
        elif val == "阳":
            val = False
        else:
            val = bool(val)
    else:
        val = bool(val)
    return val

def boolToString(val):
    if val:
        val = "true"
    else:
        val = "false"
    return val
