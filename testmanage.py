#!/usr/bin/env python

import argparse
import os
import shutil
import sys
import warnings

from django.core.management import execute_from_command_line


os.environ["DJANGO_SETTINGS_MODULE"] = "wagtail_link_field.test.settings"


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--deprecation",
        choices=["all", "pending", "imminent", "none"],
        default="imminent",
    )
    return parser


def parse_args(args=None):
    return make_parser().parse_known_args(args)


def runtests():
    args, rest = parse_args()

    only_wagtail = r"^wagtail(\.|$)"
    if args.deprecation == "all":
        warnings.simplefilter("default", DeprecationWarning)
        warnings.simplefilter("default", PendingDeprecationWarning)
    elif args.deprecation == "pending":
        warnings.filterwarnings(
            "default", category=DeprecationWarning, module=only_wagtail
        )
        warnings.filterwarnings(
            "default", category=PendingDeprecationWarning, module=only_wagtail
        )
    elif args.deprecation == "imminent":
        warnings.filterwarnings(
            "default", category=DeprecationWarning, module=only_wagtail
        )
    elif args.deprecation == "none":
        pass

    argv = [sys.argv[0]] + rest

    try:
        execute_from_command_line(argv)
    finally:
        from wagtail.test.settings import MEDIA_ROOT

        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)


if __name__ == "__main__":
    runtests()
