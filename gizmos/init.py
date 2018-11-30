import os
import nuke

dirname = os.path.dirname(os.path.abspath(__file__))

nuke.pluginAddPath(os.path.join(dirname, 'spin_tools'))
