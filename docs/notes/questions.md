---
id: wxca6y2tvdtzc9vti55idx3
title: Questions
desc: ''
updated: 1680268410226
created: 1676816641536
---
- svm.py : 

    - Training size percentage ?

    - Which normalization for each band in the hyperspectral image ? 
        - ### $\frac{value-min}{max-min}$
        - ### $\frac{value-\mu}{\sigma}$

    - GridSearchCV results : https://www.kaggle.com/code/haytamel/master-thesis/notebook

    - My workflow currently : 
        - I am working with only **one** hyperspectral image.
        - I train the model on 5% of the image's pixel.
        - I test the SVM on all the pixels of the image.
        
    - One-shot / Few-shot learning ???

- ising_model.py : 

    - Slow animation...
    - Code line 91 Problem (Test whether we accept the flip or not) ...
    - Slide 15 : Calculate local energy 
        - ### $h_i = \frac{\log(\frac{1}{P_i(C)}-1)}{4}$ 
        - For each pixel, take into account only the probability of being in class C (and not the probability of being in ¬C) ?
        - Log(0) possible ?