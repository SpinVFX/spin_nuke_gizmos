#!/usr/bin/env python
"""Build docs."""

# python
import json
import os
import subprocess
import sys


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


# setup environment
env = os.environ.copy()
env['PYTHONPATH'] = ':'.join([
    '/spin/software/python_pkg/markupsafe/1.0/python/2.7/linux/64',
    '/spin/software/python_pkg/sphinx/1.6.5/python/2.7/linux/64',
    '/spin/software/python_pkg/pygments/2.2.0/python/2.7/linux/64',
    '/spin/software/python_pkg/docutils/0.14/python/2.7/linux/64',
    '/spin/software/python_pkg/typing/3.6.2/python/2.7/linux/64',
    '/spin/software/python_pkg/babel/2.5.1/python/2.7/linux/64',
    '/spin/software/python_pkg/imagesize/0.7.1/python/2.7/linux/64',
    '/spin/software/python_pkg/alabaster/0.7.10/python/2.7/linux/64',

    # spin packages
    '/spin/software/spin3d/2.29.0/python',

]) + ':' + env['PYTHONPATH']


env['PYTHONPATH'] = os.path.join(source_root, 'build', package_version, 'python') + ':' + env['PYTHONPATH']
cmd = ['python', '-m', 'sphinx', 'doc', 'build/%s/doc' % package_version]
subprocess.check_call(cmd, env=env)

#python -m sphinx.quickstart
#python /spin/software/python_pkg/sphinx/1.6.5/python/2.7/linux/64/sphinx/quickstart.py
# python -m sphinx doc build/0.1.0/doc
