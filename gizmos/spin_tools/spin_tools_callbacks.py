"""
Add callbacks to be run on spin_tools.
"""

import nuke


def add_callbacks():
    # Add an onUserCreate callback for Chromatik in order to have the center default to the center.
    # Workaround for the fact that nuke doesn't let us set defaults on knobs properly.
    nuke.addOnUserCreate(
        lambda: nuke.thisNode()['center'].setValue((nuke.thisNode().width()/2, nuke.thisNode().height()/2)),
        nodeClass='Chromatik'
    )
