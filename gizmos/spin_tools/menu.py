"""
Creates a Spin_tools menu and dynamically populate it with .gizmo, .so and .nk files
Supports icons by adding them at the same level as the tool/subdir
All subdirectories are added to the nuke.pluginPath() (see init.py)
"""

# python
import os
import re

# nuke
import nuke

# spin_tools
import spin_tools_callbacks


DEPRECATED = 'deprecated'


# Functions
def find_icon(path, name):
    img = None
    for icon_ext in ['.jpg', '.png']:
        icon_path = os.path.join(path, name + icon_ext)
        if os.path.isfile(icon_path):
            img = icon_path
            break

    return str(img) if img else None


def populate_menu_recursive(tool_path, menu):
    if not tool_path.endswith(os.sep):
        tool_path += os.sep

    for root, dirs, files in os.walk(tool_path):
        category = root.replace(tool_path, '')
        # build the dynamic menus, ignoring empty dirs:
        for dir_name in natural_sort(dirs):
            if os.listdir(os.path.join(root, dir_name)) and dir_name != DEPRECATED:
                img = find_icon(root, dir_name)
                menu.addMenu(category + '/' + dir_name, icon=img)

        # stop here if we're in a deprecated menu
        if category == DEPRECATED:
            continue

        # if we have both dirs and files, add a separator
        if files and dirs:
            submenu = menu.addMenu(category)  # menu() and findItem() do not return a menu object.
            submenu.addSeparator()

        # Populate the menus
        for nuke_file in natural_sort(files):
            file_name, extension = os.path.splitext(nuke_file)
            if extension.lower() in ['.gizmo', '.so', '.nk']:
                img = find_icon(root, file_name)
                # Adding the menu command
                if extension.lower() in ['.nk']:
                    menu.addCommand(category + '/' + file_name,
                                    'nuke.nodePaste( "{}" )'.format(os.path.join(root, nuke_file)),
                                    icon=img)
                if extension.lower() in ['.gizmo', '.so']:
                    menu.addCommand(category + '/' + file_name,
                                    'nuke.createNode( "{}" )'.format(file_name),
                                    icon=img)
    return menu


def natural_sort(values, case_sensitive=False):
    """
    Returns a human readable list with integers accounted for in the sort.
    items = ['xyz.1001.exr', 'xyz.1000.exr', 'abc11.txt', 'xyz.0999.exr', 'abc10.txt', 'abc9.txt']
    natural_sort(items) = ['abc9.txt', 'abc10.txt', 'abc11.txt', 'xyz.0999.exr', 'xyz.1000.exr', 'xyz.1001.exr']
    :param values: string list
    :param case_sensitive: Bool. If True capitals precede lowercase, so ['a', 'b', 'C'] sorts to ['C', 'a', 'b']
    :return: list
    """
    digit_split = re.compile('([0-9]+)')

    def alpha_to_int(a, _case_sensitive=False):
        return int(a) if a.isdigit() else (a if _case_sensitive else a.lower())

    def natural_sort_key(_values):
        try:
            return tuple(alpha_to_int(c, case_sensitive) for c in digit_split.split(_values))
        except (TypeError, ValueError):
            return _values

    return sorted(values, key=natural_sort_key)


# Running code

# Finding this file's Folder
dirname = os.path.dirname((os.path.abspath(__file__)))

toolbar = nuke.toolbar("Nodes")
toolbar_spin_tools = toolbar.addMenu("Spin Tools", icon="spin_tools.png")


populate_menu_recursive(dirname, toolbar_spin_tools)


# Add Tools callbacks
spin_tools_callbacks.add_callbacks()
