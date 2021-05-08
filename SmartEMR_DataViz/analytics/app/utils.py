def clean_dict(d):
    """Remove all key, value pairs whose key is "tooltip" or whose value is either None or empty"""
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = clean_dict(v)
            if len(nested.keys()) > 0 and k != "tooltip":
                clean[k] = nested
        elif v and k != "tooltip":
            clean[k] = v
    return clean
