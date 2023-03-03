---
id: obfwtlye44igeg3v9qna8qm
title: Ising
desc: ''
updated: 1677833813467
created: 1677833535713
---
- Hamiltonian : 
    - Function that maps a string ({-1, +1}) to a real numbers.
    - Minimizing the Hamiltonian --> Solve NP complete problems.

- Quantum Ising Hamiltonian : 
    - Complicated beast ...
    - Rather than binary values --> [Pauli operators](https://en.wikiversity.org/wiki/Pauli_matrices).

- Ising Model :
    - $$H(s)=-\sum_ih_is_i-\beta\sum_{i~j}s_is_j$$
    - For a given pixel : 
        - $$h_i$$ : Likelyhood / Energy of being in a particular class.
        - $$\beta$$ : How strongly its neighboors wants it to be in their class.
    - Its basically, in terms of MRF, maximum aposteriori probability of a MRF.
    - The graph is given by a grid (Image).

- One-shot learning for the SVM...

- [Qiskit and Hamiltonian](https://qiskit.org/textbook/ch-applications/qaoa.html) 