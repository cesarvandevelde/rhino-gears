from __future__ import division
from math import tan, radians, pi
from itertools import izip
import rhinoscriptsyntax as rs

__commandname__ = "Rack"


def accumulate(l):
    total = 0
    for x in l:
        total += x
        yield total


def draw_rack(length, module, pressure_angle=20):
    pressure_angle = radians(pressure_angle)
    circular_pitch = module * pi
    tip_w = circular_pitch / 2 - 2 * module * tan(pressure_angle)

    num_instances = int((length - tip_w) / 2 / circular_pitch) + 1

    y_vals = [module]
    y_vals += [-module, -module, module, module] * num_instances
    y_vals = list(reversed(y_vals)) + y_vals

    x_vals = [tip_w / 2]
    x_vals += [circular_pitch / 2 - tip_w, tip_w] * (num_instances * 2)
    x_vals = list(accumulate(x_vals))
    x_vals = list(reversed([-x for x in x_vals])) + x_vals

    pts = [[x, y, 0] for x, y in izip(x_vals, y_vals)]

    return rs.AddPolyline(pts)


params = {
    "m":  1,
    "pa": 20
}


def RunCommand(is_interactive):
    global params

    pitch_line = rs.GetObject(message="Select pitch line",
                              filter=rs.filter.curve,
                              preselect=True)
    if pitch_line is None:
        return 1  # Cancel

    if not rs.IsLine(pitch_line):
        print "Selected curve is not a line!"
        return 1  # Cancel

    rs.SelectObjects(pitch_line)

    m = rs.GetReal(message="Rack module",
                   number=params["m"])
    pa = rs.GetReal(message="Pressure angle",
                    number=params["pa"], minimum=0, maximum=45)

    if m is None or pa is None:
        return 1  # Cancel

    params["m"] = m
    params["pa"] = pa

    pitch_line_center = rs.CurveMidPoint(pitch_line)
    pitch_line_start = rs.CurveStartPoint(pitch_line)
    pitch_line_end = rs.CurveEndPoint(pitch_line)
    angle, reflex_angle = rs.Angle2(line1=((0, 0, 0), (1, 0, 0)),
                                    line2=(pitch_line_start, pitch_line_end))

    x_vector = rs.VectorCreate(pitch_line_end, pitch_line_start)
    y_vector = rs.VectorRotate(x_vector, 90.0, [0, 0, 1])
    cplane = rs.PlaneFromFrame(origin=pitch_line_center,
                               x_axis=x_vector,
                               y_axis=y_vector)

    xform = rs.XformChangeBasis(cplane, rs.WorldXYPlane())

    rs.EnableRedraw(False)
    old_plane = rs.ViewCPlane(plane=rs.WorldXYPlane())

    rack = draw_rack(length=rs.CurveLength(pitch_line),
                     module=params["m"],
                     pressure_angle=params["pa"])

    rs.ViewCPlane(plane=old_plane)
    rs.TransformObjects(rack, xform)

    rs.EnableRedraw(True)
    rs.UnselectAllObjects()
    rs.SelectObjects(rack)

    return 0  # Success


if __name__ == "__main__":
    RunCommand(True)
