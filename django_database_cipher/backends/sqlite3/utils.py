#!/usr/bin/env python
import re
import inspect
import importlib

from django.conf import settings


def get_pragma_key():
    key = getattr(settings, 'PRAGMA_KEY', None)
    if not key:
        raise RuntimeError('Must set `PRAGMA_KEY` in settings.py')

    return key


def get_deterministic_params():
    import math
    import operator
    import django.db.backends.sqlite3.base as module
    package = 'django.db.backends.sqlite3.base'
    # module = importlib.import_module(package)
    source = inspect.getsource(module)
    none_guard = getattr(module, "none_guard")

    params = []
    match_result = re.findall(r"create_deterministic_function\('(.*?)', (\d), (.*)\)", source)
    for name, n, f in match_result:
        if f.startswith("none_guard") or f.startswith("lambda"):
            func = eval(f)

        elif f.startswith("_"):
            func = getattr(module, f)
        else:
            raise RuntimeError("un supported")

        params.append((name, int(n), func))

    return params
