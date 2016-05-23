def check_params(obj, reqs):
    for item in reqs:
        if not item in obj:
            return False
    return True