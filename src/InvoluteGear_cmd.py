from __future__ import division
import rhinoscriptsyntax as rs
from helpers import draw_gear

__commandname__ = "InvoluteGear"


params = {
    "n":  30,
    "m":  1,
    "pa": 20,
    "pc": False
}


def RunCommand(is_interactive):
    global params

    center = rs.GetPoint(message="Select center point")

    n = rs.GetInteger(message="Number of teeth",
                      number=params["n"], minimum=4)

    m = rs.GetReal(message="Gear module",
                   number=params["m"])

    pa = rs.GetReal(message="Pressure angle",
                    number=params["pa"], minimum=0, maximum=45)

    bool_opts = rs.GetBoolean(message="Output options",
                              items=(("PitchCircle", "No", "Yes"),),
                              defaults=(params["pc"],))

    if None in [center, n, m, pa, bool_opts]:
        return 1  # Cancel

    params["n"] = n
    params["m"] = m
    params["pa"] = pa
    params["pc"] = bool_opts[0]

    cplane = rs.ViewCPlane()  # Get current CPlane
    cplane = rs.MovePlane(cplane, center)
    xform = rs.XformChangeBasis(cplane, rs.WorldXYPlane())

    rs.EnableRedraw(False)
    old_plane = rs.ViewCPlane(plane=rs.WorldXYPlane())

    gear = draw_gear(teeth=params["n"],
                     module=params["m"],
                     pressure_angle=params["pa"],
                     draw_pitch_circle=params["pc"])

    rs.ViewCPlane(plane=old_plane)
    rs.TransformObjects(gear, xform)

    rs.EnableRedraw(True)
    rs.SelectObjects(gear)

    return 0  # Success


if __name__ == "__main__":
    RunCommand(True)
