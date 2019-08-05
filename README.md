# SPINVFX - Nuke Gizmos
Collection of Nuke Gizmos and Tools used in production at [SPIN VFX](http://www.spinvfx.com/).
 
### Table of Contents
**[Installation Instructions](#installation-instructions)**<br>
**[Manual Installation](#manual-installation)**<br>
**[List of Tools](#list-of-tools)**<br>
**[Thanks](#thanks)**

## Installation Instructions
For easy installation of the toolset, we provide a script that will make menu entries for each of our tools and ensure 
they are all part of the Nuke plugin path.

Installation instructions are similar for any OS. However, the paths we are using in the example are formatted for an 
UNIX system (Mac or Linux).

1. Download the full content of the spin_nuke_gizmos repository. If downloaded
as a .ZIP, uncompress the zip in the desired location. For the following steps, we will assume the folder is present 
on disk as: `/my_nuke_gizmos/spin_nuke_gizmos/`.
2. Add the path to the folder in your NUKE_PATH, either via an environment variable ([Defining Nuke plugin path](
https://learn.foundry.com/nuke/content/comp_environment/configuring_nuke/defining_nuke_plugin_path.html)) or 
via an existing/new `init.py` file, in which you would add the line: 

    ```python
    nuke.pluginAddPath('/my_nuke_gizmos/spin_nuke_gizmos/gizmos')
    ```
    
This should be enough to Install the suite of tools.


## Manual Installation
While the default installation is probably ideal for many users, it may not be the best for Studio Environments 
where tools need to be installed in a specific location or for users who already have their own Gizmo loader.

For manual installation of the tools, only the content of the `gizmos/spin_tools` folder is necessary and contains all 
the .nk and .gizmo files. 
It can be reorganized as required.

.gizmo files need to be added to the nuke plugin path. See instructions by the foundry: 
- [Loading Gizmos, Plugins, Scripts](
https://learn.foundry.com/nuke/content/comp_environment/configuring_nuke/loading_gizmos_plugins_scripts.html)
- [Custom Menus](
https://learn.foundry.com/nuke/content/comp_environment/configuring_nuke/custom_menus_toolbars.html)
 
Please note that a few gizmos are using callbacks to improve on user experience. These callbacks are defined in the 
file `/gizmos/spin_tools/spin_tools_callbacks.py` and would need to be set somewhere, though the tools will function 
without the callbacks as well.

## List of Tools

### 3D
#### Noise 3D
Generate Noise in 3D space based on Position passes. It includes pre-made Position passes for some 3D primitives, or 
can use a custom Position pass. Uses a 4D noise internally so that the 4th dimension can be used to add a 'boiling' 
effect.
#### ReProject_3D
This gizmo does camera projection using a render point position pass (in world space) and a 3D camera to 
to remap all the layers in the input image.

NOTE: The projection works best with unmatted input images or at least unpremulted matting with some coverage, 
then all masking occurs within the gizmo.
It can mask the projected image in the following ways:
- Input alpha from the 3D render.
- Projecting on surfaces facing camera, using normal (N) in world space.

Based on ReProject3D by Michael Garret.
#### Relight_Simple
Simpliflied relight node. Only requires a normal map to get started.

This node will not reproduce accurate lighting, 
as it does not take into account the actual 3D world space, but instead considers the image in its own local space.

### Color
#### Match_Black_White
Allows you to match Black and white points of an image (source) to another (Target).
#### Suppress_RGBCMY
Suppress (or boost) specific colors: Red, Green, Blue, Cyan, Magenta or Yellow.

### Comp
#### Grain_Advanced
Adds synthetic grain. The defaults are setup to resemble an HD Alexa plate's grain.
You can adjust the sliders to match a sample grain.
#### Lightwrap_Exponential
A lightwrap node with a more physical response than Nuke's default.
#### Morph_Dissolve
Allows to morph between two moving plates automatically, or can be used to improve manual Morphs.

### Effects
#### Chromatik
Chromatic aberration node using a spectral wavelength gradient.
#### Glow_Exponential
Exponential Glow node, with options to recolor and adjust falloff.

### Keying
#### Edge_Expand
Expand edges to fix fringing on keys.
#### Erode_Fine
Erode an image with fine controls, as opposed to Nuke's default erode node which can only erode full pixels.
#### Spill Correct
Use this tool to "despill" or mute colors introduced from Red/Green/Blue screens. Can replace the spill with a chosen
color.


## Thanks
Many of the tools in this collection are based on tools made available freely by the VFX community.

The resources shared by the community have been invaluable to us at Spin VFX and this collection is our first small
step in our effort to give back.

We would like to thank all of the members of the VFX community who made this possible, in particular:
- Frank Rueter, for creating and maintaining Nukepedia.
- Mads Hagbarth, for the innovating techniques shared online and the Blinkscript inspiration.
- Charles Taylor, for laying out a lot of foundations on which the current 2D team at Spin built and improved on.
- All the Compositors here at Spin who tested and suggested improvements on these tools.

Gizmos put together by Erwan Leroy.

Please enjoy.
