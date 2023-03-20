---
id: 7kax0bbzlofb4xkw773kl8x
title: Cheat_Sheet_Ising_Model
desc: ''
updated: 1679304173592
created: 1679303100940
---
- Hamiltonian : 
    - Function that maps a string ({-1, +1}) to a real numbers.
    - Minimizing the Hamiltonian --> Solve NP complete problems.
    

- Ising Model : $H(s)=-\sum_ih_is_i-\beta\sum_{i~j}s_is_j$
    - For a given pixel : 
        - $h_i$ : Likelyhood / Energy of being in a particular class.
        - $\beta$ : How strongly its neighboors wants it to be in their class (magnetic moment).
    - Its basically, in terms of MRF, maximum aposteriori probability of a MRF.
    - The graph is given by a grid (Image).


- Quantum Ising Hamiltonian : 
    - Complicated beast ...
    - Rather than binary values --> [Pauli operators](https://en.wikiversity.org/wiki/Pauli_matrices).
    - [Qiskit and Hamiltonian](https://qiskit.org/textbook/ch-applications/qaoa.html)

