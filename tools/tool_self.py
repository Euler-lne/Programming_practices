def converseBool(val):
    if len(val) == 1:
        if val == "阴":
            val = "false"
        elif val == "阳":
            val = "true"
        else:
            val = bool(val)
            if val:
                val = "true"
            else:
                val = "false"
    else:
        val = bool(val)
        if val:
            val = "true"
        else:
            val = "false"
    return val
