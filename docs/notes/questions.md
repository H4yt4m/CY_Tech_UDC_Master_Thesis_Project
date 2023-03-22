---
id: wxca6y2tvdtzc9vti55idx3
title: Questions
desc: ''
updated: 1679525259205
created: 1676816641536
---
- svm.py : 

    - Which normalization for each band in the hyperspectral image ? 
        - ## $\frac{value-min}{max-min}$
        - ## $\frac{value-\mu}{\sigma}$

    - GridSearchCV results (on another script ...)

    - For our use case, we are building an SVM, so what is the utility of the Cross Validation ? (given that, as far as I know, it is used to compare different models and then choose the best performing model to train it on the whole train dataset)  

    - My workflow currently : 
        - I am working with only **one** hyperspectral image.
        - I train the model on % of the image's pixel.
        - I test the SVM on the whole image's pixels.
        
    - Is Few-shot learning ok for our algorithm ? (15% of original df)

    - Value of gamma ...