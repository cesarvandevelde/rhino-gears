from __future__ import division
from math import tan, radians, pi
import rhinoscriptsyntax as rs
from helpers import generate_gear_crv, generate_pitch_circle_crv

__commandname__ = "HelicalGearSrf"


params = {
    "n":  30,
    "m":  1,
    "pa": 20,
    "ha": 15,
    "t": 10,
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

    ha = rs.GetReal(message="Helix angle",
                    number=params["ha"], minimum=-45, maximum=45)

    t = rs.GetReal(message="Thickness",
                   number=params["t"], minimum=0)

    bool_opts = rs.GetBoolean(message="Output options",
                              items=(("PitchCylinder", "No", "Yes"),),
                              defaults=(params["pc"],))

    if None in [center, n, m, pa, ha, t, bool_opts]:
        return 1  # Cancel

    pc = bool_opts[0]

    params["n"] = n
    params["m"] = m
    params["pa"] = pa
    params["ha"] = ha
    params["t"] = t
    params["pc"] = pc

    cplane = rs.ViewCPlane()  # Get current CPlane
    cplane = rs.MovePlane(cplane, center)
    xform = rs.XformChangeBasis(cplane, rs.WorldXYPlane())

    rs.EnableRedraw(False)
    old_plane = rs.ViewCPlane(plane=rs.WorldXYPlane())

    gear = generate_gear_crv(teeth=params["n"],
                             module=params["m"],
                             pressure_angle=params["pa"])

    pitch = abs((n * m * pi) / tan(radians(ha)))
    turns = t / pitch

    if ha < 0:
        # Left handed helix
        turns = -turns

    centerline = rs.AddLine([0, 0, 0], [0, 0, t])
    helix = rs.AddSpiral([0, 0, 0],
                         [0, 0, t],
                         pitch=pitch,
                         turns=turns,
                         radius0=(m * n) / 2)

    helical_gear_srf = rs.AddSweep2(rails=[centerline, helix], shapes=[gear])
    rs.DeleteObjects([centerline, helix, gear])

    rs.ViewCPlane(plane=old_plane)
    rs.TransformObjects(helical_gear_srf, xform)

    if pc:
        circle = generate_pitch_circle_crv(teeth=params["n"],
                                           module=params["m"])
        pitch_cyl_srf = rs.ExtrudeCurveStraight(circle,
                                                start_point=[0, 0, 0],
                                                end_point=[0, 0, t])
        rs.TransformObjects(pitch_cyl_srf, xform)
        rs.DeleteObject(circle)
        rs.SelectObjects([helical_gear_srf, pitch_cyl_srf])
    else:
        rs.SelectObjects(helical_gear_srf)

    rs.EnableRedraw(True)

    return 0  # Success


if __name__ == "__main__":
    RunCommand(True)
