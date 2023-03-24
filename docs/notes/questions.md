---
id: wxca6y2tvdtzc9vti55idx3
title: Questions
desc: ''
updated: 1679648511274
created: 1676816641536
---
- svm.py : 

    - Which normalization for each band in the hyperspectral image ? 
        - ## $\frac{value-min}{max-min}$
        - ## $\frac{value-\mu}{\sigma}$

    - GridSearchCV results : https://www.kaggle.com/code/haytamel/master-thesis/notebook

    - My workflow currently : 
        - I am working with only **one** hyperspectral image.
        - I train the model on 5% of the image's pixel.
        - I test the SVM on all the pixels of the image.
        
    - One-shot / Few-shot learning ???
