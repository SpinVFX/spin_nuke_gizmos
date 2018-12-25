"""spin tools nuke startup module.

recursively adds all subfolders to plugin path.
"""

# python
import os

# nuke
import nuke


dirname, filename = os.path.split(os.path.abspath(__file__))

for root, dirs, files in os.walk(dirname):
    nuke.pluginAddPath(root)
