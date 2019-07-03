# RhinoGears
RhinoGears is a plugin for [Rhinoceros](http;//www.rhino3d.com) that can be
used to generate custom gears. This script is partially based on
[GearGen](http://www.rayflectar.com/p04-Programming/programming.html) by Thomas
Anagnostou. However, the original GearGen is incompatible with Rhino for Mac.
RhinoGears is written in Python and is compatible with both Windows and Mac
versions of Rhino 5.

![](assets/plugin-demo.gif)

# Installation

- Download the appropriate installer file from the
[Releases](https://github.com/cesarvandevelde/rhino-gears/releases) page.
  * `RhinoGears.rhi` for Windows users
  * `RhinoGears.macrhi` for Mac users.

- Double-click to install the plugin.
  * Windows: be sure to select _"install just for me"_, not _"install for everyone"_. (see [this thread](https://www.food4rhino.com/app/rhinogears?page=2#27777) for the reason why)

- Restart Rhinoceros to make sure the plugin is loaded.

# Usage
After installation, the following commands will be available:

- `InvoluteGear` &mdash; Generate a gear curve with an involute gear tooth
  profile. Optionally also outputs the gear's pitch circle.

- `Rack` &mdash; Generate a rack curve for a rack and pinion system.

- `BevelGearSrf` &mdash; Generate a bevel (conical) gear surface with a specific
  cone angle. Optionally outputs the gear's pitch cone surface.

- `HelicalGearSrf` &mdash; Generate a helical gear surface with a specific helix
  angle. Optionally outputs the gear's pitch cylinder surface.

**Important:** There is a bug in Rhino (Win) where Python plugin commands don't
get recognized immediately in some cases. If this happens, simply run the
command `EditPythonScript` first to fix the issue. The bug is described
[here](http://developer.rhino3d.com/guides/rhinopython/creating-rhino-commands-using-python/).

## General hints

1. Gears that mesh correctly have the same module and the same pressure angle.
   In addition, their pitch circles should be tangential to one another.

2. The module of a gear determines its overall size. The diameter of a gear's
   pitch circle is equal to the module times the number of teeth.

3. The pressure angle determines the shape of the gear tooth. A higher pressure
   angle leads to stronger, noisier gear teeth. Standard values are 14.5, 20 and
   25 degrees.
