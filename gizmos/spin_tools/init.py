"""spin tools nuke startup module.

recursively adds all subfolders to plugin path.
"""

# python
import os

# scandir
import scandir

# nuke
import nuke


dirname, filename = os.path.split(os.path.abspath(__file__))

for root, dirs, files in scandir.walk(dirname):
    nuke.pluginAddPath(root)
