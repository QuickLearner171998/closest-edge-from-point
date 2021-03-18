def dot(v, w):
    x, y = v
    X, Y = w
    return x*X + y*Y


def length(v):
    x, y = v
    return math.sqrt(x*x + y*y)


def vector(b, e):
    x, y = b
    X, Y = e
    return (X-x, Y-y)


def unit(v):
    x, y = v
    mag = length(v)
    return (x/mag, y/mag)


def distance(p0, p1):
    return length(vector(p0, p1))


def scale(v, sc):
    x, y = v
    return (x * sc, y * sc)


def add(v, w):
    x, y = v
    X, Y = w
    return (x+X, y+Y)


def pnt2line(pnt, start, end):
    # create a line segment vector
    line_vec = vector(start, end)
    # create a vector from pnt to start
    pnt_vec = vector(start, pnt)
    # compute length of line vector
    line_len = length(line_vec)
    # create unit vector
    line_unitvec = unit(line_vec)
    # project pnt_vec to line_len
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    # take dot product
    t = dot(line_unitvec, pnt_vec_scaled)
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    return dist
