"""
Callbacks for Tools that are not managed by Spin, and might have come from an external source.
"""

import nuke


def edge_detect_fine_callbacks():

    """
    Disables or enables size knobs when a check box is clicked.

    :return: Callbacks for EdgeDetect Fine
    """

    node = nuke.thisNode()
    knob = nuke.thisKnob()

    if knob.name() == 'omni_gang':
        if node['omni_gang'].value():
            node['omni_size'].setEnabled(True)
            node['inside_size'].setEnabled(False)
            node['outside_size'].setEnabled(False)
        else:
            node['omni_size'].setEnabled(False)
            node['inside_size'].setEnabled(True)
            node['outside_size'].setEnabled(True)


def edge_detect_fine_auto_label():

    """
    Displays size of detection in the label

    :return: Set's label in Edge Detect Fine node
    """

    node = nuke.thisNode()

    if node.Class() == "EdgeDetect_Fine":
        user_label = nuke.tcl("subst", node['label'].value())
        if node['omni_gang'].value():
            auto_label = node.name() + '\n' + 'size ' + str(node['omni_size'].value())
            if user_label:
                auto_label = auto_label + '\n' + user_label
            return auto_label

        else:
            auto_label = node.name() + '\n' + 'in ' + str(node['inside_size'].value()) + '\n' \
                   + 'out ' + str(node['outside_size'].value())
            if user_label:
                auto_label = auto_label + '\n' + user_label
            return auto_label


def add_edge_detect_callbacks():
    nuke.addAutolabel(edge_detect_fine_auto_label, nodeClass="EdgeDetect_Fine")
    nuke.addKnobChanged(edge_detect_fine_callbacks, nodeClass="EdgeDetect_Fine")
