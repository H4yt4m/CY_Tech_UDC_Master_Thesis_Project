---
id: smy734ixyo53ughfvkqdto7
title: Thesis Writing Plan
desc: ''
updated: 1683095586275
created: 1681712756009
---
# Slides

EACH POINT IS ONE SLIDE, COULD BE DIVIDED IN THE PRESENTATION INTO MULTIPLE STEPS

- Title and me
- Supervisors
- Jury
- Goal of the project : Segmentation of hyperspectral images (satellites, healthcare, etc) using quantum annealing : General schema of before and after
- Theory : HPC characteristics (FT3 as example)
- Theory : QC : Physics theory behind it
- Theory : NP hardness HPC vs QA : Complexity theory
- Theory : QC : Gate based (briefly) vs QA Differences (JSC's D-WAVE QA as example)
- Case Study slide : Hyperspectral image segmentation
- Show initial image : This is a study image to understand the concept : On indian pines...
- Step 1 : Choose a classifier : Showcase types of classifiers, their basic and utility for our use case : Classify pixels, needed to build next weights, etc
- Overall algorithm : Initial part of the SVM
- Step 2 : Choose & Consruct our model :
- Overall algorithm : Second part of the Ising, Ising model : Presentation, use cases in physics, Relation of Ising to MRF and RBM(optional)
- Step 2 : Ensure Embedding:
- Overall algorithm : Final part of embedding and restitution
- ############### For the code details part, we can go back to it during the questions###################
- Code details : SVM (No optimization to see clear improvement, etc)
- Code details : Issues with high performance visualization of Ising
- Code details : Solution with numba as a JIT compiler + advantages (HIDE)
- Code details : Embedding to D-Wave QA and restitution
- ###########################################################################
- Results for the study image (Goal is to know that QA is WORKING, not that it is faster than classic HPC)
- Results on other hyperspectral images
- Mention the utility of numba with benchmarks with vs without numba on a small lattice with random elements generated
- Highlights my competences from this academic year in terms of AI HPC QC
- Thanks !
