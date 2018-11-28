# Creates a Spin_tools menu and dynamically populate it with .gizmo, .so and .nk files
# Supports deprecating files by moving them to a /deprecated folder (can be located anywhere)
# Supports icons by adding them either at the same level as the tool/subdir or in a /icons directory
# All subdirectories are added to the nuke.pluginPath() (see init.py)
# Supporting menus per nuke versions: add a tool in a '/nuke_v#' folder will load the tool for that version only.
# It's possible to add subfolders in a nuke_v# folder, but they will not have their icons setup


###################################################################################################
# IMPORT MODULES
###################################################################################################

# python
import os

# scandir
import scandir

# nuke
import nuke

# spin2d
from spin2d.util import get_software_version_from_path, natural_sort
from spin2d.nuke.spin_constants import NUKE_VERSION_STRING, DEPRECATED_FOLDER, ICONS_FOLDER

# spin_tools
import spin_tools_callbacks


###################################################################################################
# Functions
###################################################################################################


def find_icon(path, name):
    img = None
    for icon_ext in ['.jpg', '.png']:
        icon_path = os.path.join(path, name + icon_ext)
        if os.path.isfile(icon_path):
            img = icon_path
        else:
            icon_path = os.path.join(path, ICONS_FOLDER, name + icon_ext)
            if os.path.isfile(icon_path):
                img = icon_path

    return str(img) if img else None


def populate_menu_rcsv(tool_path, menu, hotkeys=None):
    # Define Hotkeys as gizmo:hotkey pairs IE. hotkeys = {'CamQuake': 'ctrl+shift+K'}
    if not hotkeys:
        hotkeys = {}
    if not tool_path.endswith(os.sep):
        tool_path += os.sep

    for root, dirs, files in scandir.walk(tool_path):
        category = root.replace(tool_path, '')
        # build the dynamic menus, ignoring empty or deprecated dirs:
        for d in natural_sort(dirs):
            if os.listdir(os.path.join(root, d)):
                if d not in [DEPRECATED_FOLDER, ICONS_FOLDER]:
                    nuke_version_in_path = get_software_version_from_path(os.path.join(category, d))
                    if not nuke_version_in_path:  # Ignoring folders within nuke versions
                        img = find_icon(root, d)
                        menu.addMenu(os.path.join(category, d), icon=img)

        # if we have both dirs and files, add a separator
        if files and dirs:
            submenu = menu.addMenu(category)  # menu() and findItem() do not return a menu object.
            submenu.addSeparator()

        if not root.endswith(DEPRECATED_FOLDER):
            # Populate the menus
            nuke_version_in_path = get_software_version_from_path(category)
            if not nuke_version_in_path or nuke_version_in_path == NUKE_VERSION_STRING:
                category = category.replace('/{}'.format(NUKE_VERSION_STRING), '')
                for f in natural_sort(files):
                    f_name, ext = os.path.splitext(f)
                    if ext.lower() in ['.gizmo', '.so', '.nk']:
                        img = find_icon(root, f_name)
                        # Setting the keyboard shortcut
                        hotkey = ''
                        if f_name in hotkeys.keys():
                            hotkey = hotkeys[f_name]
                        # Adding the menu command
                        if ext.lower() in ['.nk']:
                            menu.addCommand(os.path.join(category, f_name), 'nuke.nodePaste( "{}" )'.format(os.path.join(root, f)),
                                            icon=img, shortcut=hotkey, shortcutContext=2)
                        if ext.lower() in ['.gizmo', '.so']:
                            menu.addCommand(os.path.join(category, f_name), 'nuke.createNode( "{}" )'.format(f_name), icon=img,
                                            shortcut=hotkey, shortcutContext=2)
    return menu


###################################################################################################
# Running code
###################################################################################################

# Finding this file's Folder
dirname, filename = os.path.split(os.path.abspath(__file__))

toolbar = nuke.toolbar("Nodes")
toolbar_spin_tools = toolbar.addMenu("Spin Tools", icon="spin_tools.png")


populate_menu_rcsv(dirname, toolbar_spin_tools)

spin_tools_callbacks.add_callbacks()
