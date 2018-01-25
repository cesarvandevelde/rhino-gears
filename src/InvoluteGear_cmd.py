from __future__ import division
from math import sin, cos, asin, atan, radians, degrees, pi, sqrt
import rhinoscriptsyntax as rs

__commandname__ = "InvoluteGear"


def draw_gear(teeth,
              module,
              pressure_angle=20,
              draw_pitch_circle=False,
              clearance=0.167,
              involute_samples=5):
    pressure_angle = radians(pressure_angle)

    pitch_diam = module * teeth
    base_circle = pitch_diam * cos(pressure_angle)
    addendum = module
    dedendum = (1 + clearance) * module
    outside_diam = pitch_diam + 2*addendum
    root_diam = pitch_diam - 2*dedendum
    chordal_thickness = pitch_diam * sin((pi/2)/teeth)

    invol_start_angle = (pi/2 + asin(chordal_thickness/pitch_diam)
                         - pressure_angle
                         + sqrt((pitch_diam/base_circle)**2 - 1))
    invol_end_angle = (invol_start_angle
                       - sqrt((outside_diam/base_circle)**2 - 1))

    if root_diam > base_circle:
        invol_angle_mod = sqrt((root_diam/base_circle)**2 - 1)
    else:
        invol_angle_mod = 0

    invol_pts = []
    step = invol_start_angle - invol_angle_mod - invol_end_angle
    step = step / involute_samples

    # Calculate involute
    for i in xrange(involute_samples + 1):
        pos = i * step
        invol_height = sqrt((pos + invol_angle_mod)**2 * (base_circle/2)**2
                            + (base_circle/2)**2)
        invol_height_angle = (invol_start_angle - invol_angle_mod - pos
                              + atan(pos + invol_angle_mod))

        pt = [invol_height * cos(invol_height_angle),
              invol_height * sin(invol_height_angle),
              0]
        invol_pts.append(pt)

    tooth_crvs = []

    invol_crv1 = rs.AddInterpCurve(invol_pts, degree=3, knotstyle=1)
    invol_crv2 = rs.MirrorObject(invol_crv1, [0, 0, 0], [0, 1, 0], copy=True)
    top_arc = rs.AddArc3Pt(start=rs.CurveEndPoint(invol_crv1),
                           end=rs.CurveEndPoint(invol_crv2),
                           point_on_arc=[0, outside_diam/2, 0])

    tooth_crvs.append(invol_crv1)
    tooth_crvs.append(invol_crv2)
    tooth_crvs.append(top_arc)

    # Dedendum
    if root_diam < base_circle:
        pt = [root_diam/2 * cos(invol_start_angle),
              root_diam/2 * sin(invol_start_angle),
              0]
        ded_crv1 = rs.AddLine(rs.CurveStartPoint(invol_crv1), pt)
        ded_crv2 = rs.MirrorObject(ded_crv1, [0, 0, 0], [0, 1, 0], copy=True)

        tooth_crvs.append(ded_crv1)
        tooth_crvs.append(ded_crv2)

    tooth = rs.JoinCurves(tooth_crvs, delete_input=True)[0]

    # Tooth bottom
    angle = 2*pi/teeth
    start_pt = rs.CurveStartPoint(tooth)
    end_pt = rs.CurveEndPoint(tooth)
    end_pt = [end_pt[0]*cos(angle) - end_pt[1]*sin(angle),
              end_pt[1]*cos(angle) + end_pt[0]*sin(angle),
              0]
    pt_on_arc = [-sin(angle/2) * (root_diam/2),
                 cos(angle/2) * (root_diam/2),
                 0]
    bottom_arc = rs.AddArc3Pt(start_pt, end_pt, pt_on_arc)

    tooth = rs.JoinCurves([tooth, bottom_arc], delete_input=True)[0]

    # Copy and rotate tooth N times
    crvs = [tooth]
    for i in xrange(1, teeth):
        crv = rs.RotateObject(tooth, [0, 0, 0], degrees(i*angle), copy=True)
        crvs.append(crv)

    crvs = rs.JoinCurves(crvs, delete_input=True)
    if draw_pitch_circle:
        crv = rs.AddCircle([0, 0, 0], pitch_diam/2)
        crvs.append(crv)

    return crvs


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
