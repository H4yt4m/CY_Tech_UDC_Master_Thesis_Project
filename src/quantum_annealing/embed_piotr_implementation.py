from collections import namedtuple
from itertools import product

Point = namedtuple("Point", "x, y")
Size = namedtuple("Size", "xdim, ydim")


def twodim_to_ord(point, size):
    point = Point(*point)
    size = Size(*size)
    return point.x * size.ydim + point.y


def pixel_address(cluster_x, cluster_y, inside_x, inside_y):
    if cluster_x % 2 == 0 and cluster_y % 2 == 0:
        address = inside_y * 2 + inside_x
    elif cluster_x % 2 == 1 and cluster_y % 2 == 0:
        address = inside_y * 2 - inside_x + 1
    elif cluster_x % 2 == 0 and cluster_y % 2 == 1:
        address = (1 - inside_y) * 2 + inside_x
    elif cluster_x % 2 == 1 and cluster_y % 2 == 1:
        address = (1 - inside_y) * 2 + 1 - inside_x
    cluster_start = cluster_x * 8 + cluster_y * 8 * 16
    return {cluster_start + address, cluster_start + address + 4}


def pixel_embedding(x, y):
    cluster_x, cluster_y = x // 2, y // 2
    inside_x, inside_y = x % 2, y % 2
    return pixel_address(cluster_x, cluster_y, inside_x, inside_y)


def grid_embedding(size_x=32, size_y=32):
    embedding_dict = {}
    size = Size(size_x, size_y)
    for x, y in product(range(size_x), range(size_y)):
        i = twodim_to_ord((y, x), size)
        embedding_dict[i] = pixel_embedding(x, y)
    return embedding_dict
