# Credits : 
# https://github.com/syamkakarla98/Hyperspectral_Image_Analysis_Simplified
# https://medium.com/@pushkarmandot/what-is-the-significance-of-c-value-in-support-vector-machine-28224e852c5a

# Data sources : 
# http://www.ehu.eus/ccwintco/uploads/6/67/Indian_pines_corrected.mat
# http://www.ehu.eus/ccwintco/uploads/c/c4/Indian_pines_gt.mat

import sys
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from scipy.io import loadmat

#!wget http://www.ehu.eus/ccwintco/uploads/6/67/Indian_pines_corrected.mat http://www.ehu.eus/ccwintco/uploads/c/c4/Indian_pines_gt.mat

def read_files(HSI_path, GT_path):
    X = loadmat(HSI_path)[HSI_path.replace('/', '.').split('.')[-2].split()[0].lower()]
    y = loadmat(GT_path)[GT_path.replace('/', '.').split('.')[-2].split()[0].lower()]
    print(f"\nX shape: {X.shape}\ny shape: {y.shape}\n")
    return X, y

def extract_pixels_one_vs_all_classes(X, y, class_number):
    q = X.reshape(-1, X.shape[2])
    df = pd.DataFrame(data = q)
    temp = y.ravel()
    for i in range(len(temp)):
        if temp[i]!=class_number :
            temp[i] = class_number+10
    df = pd.concat([df, pd.DataFrame(data = temp)], axis=1)
    df.columns= [f'band{i}' for i in range(1, 1+X.shape[2])]+['class']
    df.to_csv('Dataset.csv')
    return df, np.reshape(temp, (145,145))

def split_into_train_test(df, test_percentage):
    x = df[df['class'] != 0]
    X = x.iloc[:, :-1].values
    y = x.loc[:, 'class'].values 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_percentage, random_state=11, stratify=y)
    return X_train, X_test, y_train, y_test

def plot_image(y, fig_name):
    plt.figure(figsize=(10, 8))
    plt.imshow(y, cmap='nipy_spectral')
    plt.colorbar()
    plt.axis('off')
    plt.savefig(fig_name)
    plt.show()
    
def normalize_data(data):
    # todo
    return normalized_data

def main():
    # SVM
    X, y = read_files('./Indian_pines_corrected.mat', './Indian_pines_gt.mat')
    df, y = extract_pixels_one_vs_all_classes(X, y, 11)
    # Ques : Value of test ratio ?
    X_train, X_test, y_train, y_test = split_into_train_test(df, 0.2)
    # Ques : Value of C ? kernel ? cache_size ?
    svm =  SVC(C = 100, kernel = 'rbf', cache_size = 10*1024)
    svm.fit(X_train, y_train)

    # Ques : Useful ?
    # ypred = svm.predict(X_test)

    l=[]
    for pixel in range(df.shape[0]):
        # if df.iloc[pixel, -1] == 21:
        #     l.append(21)
        # else:
        #     l.append(svm.predict(df.iloc[pixel, :-1].values.reshape(1, -1)))
        l.append(svm.predict(df.iloc[pixel, :-1].values.reshape(1, -1)))
    clmap = np.array(l).reshape(145, 145).astype('float')

    print("\n Ground Truth : \n")
    plot_image(y, 'IP_GT.png')
    print("\n Prediction : \n")
    plot_image(clmap, 'IP_cmap.png')
    return 0

if __name__ == '__main__':
    sys.exit(main())