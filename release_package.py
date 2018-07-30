#!/usr/bin/env python

# python
import json
import grp
import os
import shutil
import sys

# get release mode
release_mode = 'local'
release_gid = None
if len(sys.argv) == 2 and sys.argv[1] == '-r':
    release_mode = 'spin'
    release_gid = grp.getgrnam('prod_eng_dev').gr_gid

source_root = os.path.dirname(os.path.realpath(__file__))
# ensure we are running from package root
cwd = os.path.realpath(os.getcwd())
if cwd != source_root:
    sys.stdout.write('ERROR: must run build script from source package root\n')
    sys.exit(1)

# read manifest for package name, version:
manifest_path = os.path.join(source_root, 'manifest')
with open(manifest_path) as f:
    manifest = json.load(f)
package_name = manifest['name']
package_version = manifest['version']

staging_path = os.path.join(source_root, 'build', package_version)
if not os.path.exists(staging_path):
    sys.stdout.write('ERROR: you must build the package to the staging area first\n')
    sys.exit(1)

def set_write(path):

    stat = os.stat(path)
    os.chmod(path, stat.st_mode | 0200)

    child_names = os.listdir(path)
    for child_name in child_names:
        child_path = os.path.join(path, child_name)
        if os.path.isdir(child_path):
            set_write(child_path)
        elif os.path.isfile(child_path):
            stat = os.stat(child_path)
            yes_write = stat.st_mode | 0200
            os.chmod(child_path, yes_write)
        else:
            raise RuntimeError('something other than file or dir not handled')

if release_mode == 'spin':
    target_path = os.path.expandvars('/spin/software/%s/%s' % (package_name, package_version))
else:
    target_path = os.path.expandvars('$HOME/software/%s/%s' % (package_name, package_version))

if os.path.exists(target_path):
    if release_mode == 'spin':
        sys.stdout.write('ERROR: a release already exists in target dir %s\n' % target_path)
        sys.exit(1)

    # overwrite local install
    set_write(target_path)
    shutil.rmtree(target_path)

# copy it
shutil.copytree(staging_path, target_path,
                ignore=shutil.ignore_patterns('*.pyc'))

def set_read_only(path, release_gid):
    """Set file tree read-only."""

    child_names = os.listdir(path)
    for child_name in child_names:
        child_path = os.path.join(path, child_name)
        if os.path.isdir(child_path):
            if release_gid is not None:
                os.chown(child_path, -1, release_gid)
            set_read_only(child_path, release_gid)
        elif os.path.isfile(child_path):
            if release_gid is not None:
                os.chown(child_path, -1, release_gid)
            stat = os.stat(child_path)
            no_write = stat.st_mode & ~(0222)
            os.chmod(child_path, no_write)
        else:
            raise RuntimeError('something other than file or dir not handled')

    if release_gid is not None:
        os.chown(path, -1, release_gid)

    stat = os.stat(path)
    no_write = stat.st_mode & ~(0222)
    os.chmod(path, no_write)


# set everything read-only
set_read_only(target_path, release_gid)

sys.stdout.write('\nSUCCESS: installed to %s\n\n' % target_path)
