import dwave_networkx as dnx
from embed_my_implementation import *
from embed_piotr_implementation import *
import matplotlib.pyplot as plt

size = 145
rows = size
columns = size
lattice_size = size
beta = 0.5

# # COMMENT ONE OF THE TWO ##############################################################################################

# # Piotr implemented embedding #########################################################################################
type = "piotr_implemented_embedding_{}_{}".format(rows, columns)
embedding = grid_embedding(rows, columns)

# # My implemented embedding ############################################################################################
# type = "my_implemented_embedding_{}_{}".format(rows, columns)
# embedding = grid_to_chimera(rows, columns)

# #######################################################################################################################

chimera = dnx.chimera_graph(size)
dnx.draw_chimera_embedding(
    chimera,
    emb=embedding,
    with_labels=False,
    width=0.025,
    node_size=0,
    alpha=1,
)
plt.savefig(type, dpi=2000)
