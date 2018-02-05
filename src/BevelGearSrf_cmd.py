from __future__ import division
from math import tan, radians
import rhinoscriptsyntax as rs
from helpers import generate_gear_crv, generate_pitch_circle_crv

__commandname__ = "BevelGearSrf"


params = {
    "n":  30,
    "m":  1,
    "pa": 20,
    "ca": 90,
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

    ca = rs.GetReal(message="Cone angle",
                    number=params["ca"], minimum=0, maximum=180)

    bool_opts = rs.GetBoolean(message="Output options",
                              items=(("PitchCone", "No", "Yes"),),
                              defaults=(params["pc"],))

    if None in [center, n, m, pa, ca, bool_opts]:
        return 1  # Cancel

    pc = bool_opts[0]

    params["n"] = n
    params["m"] = m
    params["pa"] = pa
    params["ca"] = ca
    params["pc"] = pc

    cplane = rs.ViewCPlane()  # Get current CPlane
    cplane = rs.MovePlane(cplane, center)
    xform = rs.XformChangeBasis(cplane, rs.WorldXYPlane())

    rs.EnableRedraw(False)
    old_plane = rs.ViewCPlane(plane=rs.WorldXYPlane())

    gear = generate_gear_crv(teeth=params["n"],
                             module=params["m"],
                             pressure_angle=params["pa"],
                             cone_angle=params["ca"])

    # Calculate pitch cone tip
    cone_tip = [0, 0, (m * n / 2) * tan(radians(ca/2))]
    bevel_gear_srf = rs.ExtrudeCurvePoint(gear, cone_tip)

    rs.ViewCPlane(plane=old_plane)
    rs.TransformObjects(bevel_gear_srf, xform)

    if pc:
        circle = generate_pitch_circle_crv(teeth=params["n"],
                                           module=params["m"])
        pitch_cone_srf = rs.ExtrudeCurvePoint(circle, cone_tip)
        rs.TransformObjects(pitch_cone_srf, xform)
        rs.DeleteObjects([gear, circle])
        rs.SelectObjects([bevel_gear_srf, pitch_cone_srf])
    else:
        rs.DeleteObject(gear)
        rs.SelectObjects(bevel_gear_srf)

    rs.EnableRedraw(True)

    return 0  # Success


if __name__ == "__main__":
    RunCommand(True)
