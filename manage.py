#!/usr/bin/env python
import os, sys

path = '/var/www/apps/'
if path not in sys.path:
    sys.path.append(path)

if __name__ == "__main__":
    os.environ.setdefault("PYTHONPATH", "/var/www/apps/collaborate/current")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
