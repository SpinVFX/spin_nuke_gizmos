"""spin tools nuke startup module.

recursively adds all subfolders to plugin path.
"""


# python
import os

# scandir
import scandir

# nuke
import nuke

# spin2d
from spin2d.util import get_software_version_from_path
from spin2d.nuke.spin_constants import NUKE_VERSION_STRING


dirname, filename = os.path.split(os.path.abspath(__file__))

for root, dirs, files in scandir.walk(dirname):
    relative_path = root.replace(dirname, '')
    nuke_version_in_path = get_software_version_from_path(relative_path)
    if not nuke_version_in_path or nuke_version_in_path == NUKE_VERSION_STRING:
        nuke.pluginAddPath(root)
