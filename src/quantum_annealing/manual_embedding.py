import dwave_networkx as dnx
import math


def grid_to_chimera(lR, lC):
    """
    Embed a grid into chimera graph
    """

    embedding = {}
    coords = dnx.chimera_coordinates(lR, lC, 4)

    for x in range(lR):
        for y in range(lC):
            embedding[x * lR + y] = []

            candidate_chain = spin_to_chimera(x, y)

            embedding[x * lR + y].extend(
                (
                    coords.chimera_to_linear(candidate_chain[0]),
                    coords.chimera_to_linear(candidate_chain[1]),
                )
            )

    return dict(sorted(embedding.items(), key=lambda item: item[1]))


def spin_to_chimera(x, y):
    chimera_node_ids = []

    i = math.floor(x / 2)
    j = math.floor(y / 2)
    k = (i % 2) + (x % 2) * (-1) ** (i % 2) + 2 * ((j % 2) + (y % 2) * (-1) ** (j % 2))

    chimera_node_ids.append((i, j, 0, k))
    chimera_node_ids.append((i, j, 1, k))

    return chimera_node_ids
