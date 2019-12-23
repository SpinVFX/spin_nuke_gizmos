"""
Add callbacks to be run on spin_tools.
"""

import nuke


def center_chromatik():
    try:
        node_format = nuke.selectedNode()
    except ValueError:
        node_format = nuke.root()['format'].value()
    nuke.thisNode()['center'].setValue((node_format.width() / 2, node_format.height() / 2))


def add_callbacks():
    # Add an onUserCreate callback for Chromatik in order to have the center default to the center.
    # Workaround for the fact that nuke doesn't let us set defaults on knobs properly.
    nuke.addOnUserCreate(
        center_chromatik,
        nodeClass='Chromatik'
    )
