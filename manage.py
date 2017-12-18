#!/usr/bin/env python3
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.dreamrich.settings")
    if len(sys.argv) >= 2:
        print("""
____________________________________________
   ___                       ___  _     __
  / _ \\_______ ___ ___ _    / _ \\(_)___/ /
 / // / __/ -_) _ `/  ' \\  / , _/ / __/ _ \\
/____/_/  \\__/\\_,_/_/_/_/ /_/|_/_/\\__/_//_/
--------------------------------------------
____________________________________________
Copyright 2017 - Dreamrich Software

""")
    try:
        from django.core.management import execute_from_command_line

    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # NOQA
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
