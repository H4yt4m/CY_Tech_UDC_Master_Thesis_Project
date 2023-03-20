---
id: 8xmaqjhg745j8yq9z7ekew9
title: Cheat_Sheet_Markov_Random_Field
desc: ''
updated: 1679328619007
created: 1679303558361
---
- Also known as Markov Network.
- Undirected graph.
- **Node** : Discrete or Gaussian Probability distribution of random variables.
- **Edge** : Strength of the dependence between both variables.
- Main difference with a Bayesian Network : 
    - MRF are undirected, while a Bayesian Network is directed. 
- It satisfies : $p(u_i | \{u_j \}_{j∈V-i}) = p(u_i | \{u_j \}_{j∈N-i} )$
- The distribution over an MRF can be expressed in terms of energy function : 
    - $p(u) =(1/Z)*exp(−E(u, θ))$ **with :** $E(u, θ) = \sum_{c\in C }Ψ_c(ū_c,θ_c)$
    - Minimizing **E** is maximizing **p**
- Partition function : $\sum_{u_1, .. , u_N}\prod_{c\in C}{exp(−Ψ_c(ū_c,θ_c))}$
- Energy expression : $E(u) = E_{data}(u) + E_{smoothness}(u)$
    - Data term : 
        - Consistency of the model with the measurement data
        - Penalizes discrepancy.
    - Smoothness term : 
        - Derived from prior knowledge about plausible solutions.
    - It is equal to the negative log posterior, up to a constant.
- The posterior of a given RV $U_i$, with respect to all other RV in the graph, is equal to the posterior with respect to RV in the Markov Blanket of node i (ie. neighbors).
    - Thus, information **propagates** through the graph, thanks to local connections.
- Conditional independence : ${\displaystyle P(A\mid B,C)=P(A\mid C)}$ ...
- Maximal clique : Maximal fully connected subset of nodes.
- Factorization of the joint distribution ?