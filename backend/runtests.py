#!/usr/bin/env python
"""
Entrypoint to run Django tests in CI focusing only on backend.
Usage:
  python runtests.py
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    failures = test_runner.run_tests(["api"])
    sys.exit(bool(failures))

if __name__ == "__main__":
    main()
