#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bigflow.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    execute_from_command_line(sys.argv)


#1.when change a supplier in pr maker rate may not change after clicking a +
#2.when adding a two ccbs for a single detail its a issue
#3.po maker has 0.00 when delete and save
#4.pr maker when insert a dropdown data fastly it inserted