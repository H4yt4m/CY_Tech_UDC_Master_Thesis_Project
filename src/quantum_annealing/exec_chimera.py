import dimod
from dwave.system import FixedEmbeddingComposite
from construct_ising import *

from draw_chimera import *

from dimod.serialization.format import Formatter

# ising coefficient
lattice_size = 145
beta = 0.5
probabilities = np.loadtxt("probabilities.txt", dtype=float, delimiter=" ")
external_field, neighbors_coupling = hamiltonian(lattice_size, beta, probabilities)


# size is in draw_chimera
chimera = dnx.chimera_graph(size, size, 4)
structured_sampler = dimod.StructureComposite(
    dimod.SimulatedAnnealingSampler(), chimera.nodes, chimera.edges
)

# # COMMENT ONE OF THE TWO ##############################################################################################

# # My implemented embedding ############################################################################################
# type = "my_implemented_embedding_{}_{}".format(rows, columns)
# embedding = grid_to_chimera(rows, columns)

# # Piotr implemented embedding #########################################################################################
type = "piotr_implemented_embedding_{}_{}".format(rows, columns)
embedding = grid_embedding(rows, columns)

# #######################################################################################################################


sampler = FixedEmbeddingComposite(structured_sampler, embedding)

sampleset = sampler.sample_ising(
    external_field,
    neighbors_coupling,
    num_reads=1,
    label="final",
)

print(sampleset.first)
# Formatter(width=45).fprint(sampleset)
