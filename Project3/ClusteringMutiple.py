import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from matplotlib import pyplot as py
#________________________________________________________________________________________
# Name: George Shea     ßeta
# Date Created: 16/11/21
# Date Modified 16/11/21
# 2 diffrent methods comparedx
# Version 0.0
#________________________________________________________________________________________


# Used To Locate File And Normalize Its Contents
def Reader():
    # Edit This To Change Path On Your Local Machine To Wear The file is Located
    # 'Destop' comma  'exampleFolder comma AnotherFolder Comma AtualData.csv
    path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Data', 'client_data.xlsx')
    extentsion = path.split(".")[1]

    # Supported Formats xlsx and csv
    if (extentsion == "xlsx"):
        path = pd.ExcelFile(path)
        dataFramePrime = pd.read_excel(path)
        dataFramePrime = dataFramePrime.drop(("Company"), axis=1)   # Drops Company Names
        dataFramePrime = (dataFramePrime - dataFramePrime.mean()) / dataFramePrime.std()    # Data Normalizer
        return dataFramePrime
    if (extentsion == "csv"):
        dataFramePrime = pd.read_csv(path)
        dataFramePrime = dataFramePrime.drop(("Company"), axis=1)
        dataFramePrime = (dataFramePrime - dataFramePrime.mean()) / dataFramePrime.std()
        return dataFramePrime
    else: return None


def KPrinter():
    data = Reader()

    # "Classifer" is made out of sales and years in business
    # You can choice any 2 you want. I choice years and buisness and sales as i thought that made sense
    classifer = data.iloc[::, [2,3]]
    inert = []  # stores SS2 Scores refered to as inertia by sklearn
    counter = 1 # starts cluster count at 1
    while counter <= 10:
        kmeans = KMeans(n_clusters=counter, random_state=0).fit(classifer)
        kmeans.labels_  # dont delete
        inert.append(kmeans.inertia_)
        counter = counter + 1

    py.plot(inert)
    py.show()

def HPrinter():
    # https://scikit-learn.org/stable/modules/clustering.html
    data = Reader()

    # "Classifer" is made out of sales and years in business
    # You can choice any 2 you want. I choice years and buisness and sales as i thought that made sense
    classifer = data.iloc[::, [2,3]]

    # You can choice between complete single or average, though in this istance we have been asked to use complete
    linked = linkage(classifer, 'complete') # linkage preformce the clustering for us
    dendrogram(linked, orientation='top', distance_sort='descending')   # organizes the coresponding into a pleasing shape
    plt.show()  # shows dendo gram


# Experimental 
def DBSanPrinter():
    data = Reader()
    print("_____________________________________________")
    classifer = data.iloc[::, [2,3]]


    clustering = DBSCAN(eps=.6, min_samples=4).fit(classifer)
    clustering.labels_
    print(clustering.labels_)

    py.plot(clustering.labels_)
    py.plot(classifer)
    py.show()

KPrinter()
HPrinter()

#DBSanPrinter()
