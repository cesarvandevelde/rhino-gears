# RhinoGears
RhinoGears is a plugin for [Rhinoceros](http;//www.rhino3d.com) that can be
used to generate custom gears. This script is partially based on [GearGen](http://www.rayflectar.com/p04-Programming/programming.html) by Thomas Anagnostou. However, the original GearGen is incompatible with Rhino for Mac. RhinoGears is written in Python and is compatible with both Windows and Mac versions of Rhino 5.

![](assets/plugin-demo.gif)

# Installation
Download the appropriate file from the Releases page, `RhinoGears.rhi` for Windows users or `RhinoGears.macrhi` for Mac users. Double-click to install the plugin automatically. Restart Rhinoceros to make sure the plugin is loaded.

# Usage
After installation, the following commands will be available:

- `InvoluteGear` &mdash; Generate a gear curve with an involute gear tooth profile. Optionally also outputs the gear's pitch circle.

- `Rack` &mdash; Generate a rack curve for a rack and pinion system.

## General hints

1. Gears that mesh correctly have the same module and the same pressure angle. In addition, their pitch circles should be tangential to one another.

2. The module of a gear determines its overall size. The diameter of a gear's pitch circle is equal to the module times the number of teeth.

3. The pressure angle determines the shape of the gear tooth. A higher pressure angle leads to stronger, noisier gear teeth. Standard values are 14.5, 20 and 25 degrees.
