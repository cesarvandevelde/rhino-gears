from __future__ import division
from math import sin, cos, asin, atan, radians, degrees, pi, sqrt
import rhinoscriptsyntax as rs


def generate_involute_pts(base_circle_diam, start_angle, end_angle, samples):
    pts = []
    step = (start_angle - end_angle) / samples

    # Calculate involute
    for i in xrange(samples + 1):
        pos = i * step
        height = sqrt(pos**2 * (base_circle_diam/2)**2
                      + (base_circle_diam/2)**2)
        height_angle = start_angle - pos + atan(pos)

        pt = [height * cos(height_angle), height * sin(height_angle), 0]
        pts.append(pt)

    return pts


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

    invol_pts = generate_involute_pts(
                    base_circle_diam=base_circle,
                    start_angle=invol_start_angle - invol_angle_mod,
                    end_angle=invol_end_angle,
                    samples=involute_samples)

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
