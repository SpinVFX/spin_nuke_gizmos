#!/usr/bin/env python
"""Create package for install/release."""

# python
import json
import logging as log
import os
import shutil
import subprocess
import sys

# setup logging
log.basicConfig(
    format='%(message)s',
    level=log.INFO
)

source_root = os.path.dirname(os.path.realpath(__file__))
# ensure we are running from package root
cwd = os.path.realpath(os.getcwd())
if cwd != source_root:
    sys.stdout.write('must run build script from source package root')
    sys.exit(1)

# read manifest for package name, version:
manifest_path = os.path.join(source_root, 'manifest')
with open(manifest_path) as f:
    manifest = json.load(f)
package_name = manifest['name']
package_version = manifest['version']

def ensure_directory(path):
    """Ensure a directory exists."""
    # TODO: ensure is a directory, that we can write (race), etc.
    if not os.path.exists(path):
        os.makedirs(path)

target_root = os.path.join(source_root, 'build', package_version)
if os.path.exists(target_root):
    shutil.rmtree(target_root)
ensure_directory(target_root)

# first copy the python package dir
shutil.copytree(os.path.join(source_root, 'gizmos'),
                os.path.join(target_root, 'gizmos'),
                ignore=shutil.ignore_patterns('*.pyc', '*~'))
