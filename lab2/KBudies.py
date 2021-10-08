import pandas as pd                         # Used for dataframes
from sklearn.utils import shuffle           # Shuffles dataframe
from math import sqrt                       # Knn calculation
import numpy as np                          # Math calculation
from matplotlib import pyplot as plt        # For plotting
import time                                 # Used for calculating duration of calculation


#________________________________________________________________________________________
# Name: George Shea     ßeta
# Date Created: 6/10/21
# Date Modified 8/10/21
# Lab 2 find knn for give data
# Version 2.3
#________________________________________________________________________________________

# put your path here
path = ('C:/Users/gshea/Desktop/School/Summer2021/Artifical/DataSets/fruits_classification.xlsx')

extentsion = path.split(".")[1]
if (extentsion == "xlsx"):
    path = pd.ExcelFile(path)
    dataFramePrime = pd.read_excel(path)
if (extentsion == "csv"):
    dataFramePrime = pd.read_csv(path)

def Primer(k=None, dataStart=None, dataEnd=None, classifer=None, split=None):
    # Cuts out defined data
    endOf = dataFramePrime.iloc[:, dataStart:dataEnd+1]
    # Runs normaliztion on defined data
    endOf = (endOf - endOf.mean()) / endOf.std()
    # gets start of data
    startOF = dataFramePrime.iloc[:, :dataStart]
    # Combinds and shuffles data
    result = startOF.join(endOf)
    normalizedDf = shuffle(result)

    # splits data at a 60/40 split
    train = normalizedDf.sample(frac=split)
    test = normalizedDf.drop(train.index)

    #Find friends up the ladder
    average = FindFriends(train, test, k, dataStart, dataEnd, classifer)
    return average

def FindFriends(train, test, k=None, dataStart=None, dataEnd=None, classifer=None):
    # 1 goes through test data and does k nearest for each training data
    # 2 using knn makes a guess
    # 3 finnaly average correct guess verses total

    testCounter = 0
    matchCount = 0

    # Goes through each item in test
    for index, rowTest in test.iterrows():
        # Resets the following values for each instance of test
        topFriends = []
        friends = []
        friendsIndex = []
        trainCounter = 0
        # Will go through each istance of test and do knn with all training data
        for index, rowTrain in train.iterrows():
            # KNN function can be n length
            value = 0
            s = dataStart
            while s <= dataEnd:
                value = value + ((train.iloc[trainCounter::, s].values[0] - test.iloc[testCounter::, s].values[0])**2)
                s = s + 1

            # Adds neighbor and its index to the list
            friends.append(sqrt(value))
            friendsIndex.append((trainCounter))

            trainCounter = trainCounter + 1

        # F is the nearest neighbor value, fI is its index in the larger train data set.
        fI, f = np.array(friendsIndex), np.array(friends)
        # Sorts F into shortest to longest distance and than matchs fI to that organzation
        inds = f.argsort()
        fI, f = fI[inds], f[inds]

        #Gets top neighbors based on k
        i = 0
        while i <= k:
            topFriends.append(train.iloc[fI[i], classifer])
            i = i + 1

        # Runs MostFrequent function will average the postion of same classifer and return the shorts average as its guess
        guess = MostFrequent(topFriends, f[:k])

        # If right + 1 else nothing
        if(test.iloc[testCounter, classifer] == guess):
            matchCount = matchCount + 1

        testCounter = testCounter + 1

    # finally returns average
    return round(matchCount / len(test) * 100, 2)

def MostFrequent(listCount, fI):
    # Creates a tuple of f(knn distance) fI index
    mergedList = [(fI[i], listCount[i]) for i in range(0, len(fI))]
    output = {}

    # Created dic and sorts by classifer
    for x, y in mergedList:
        if y in output:
            output[y].append((x, y))
        else:
            output[y] = [(x, y)]

    test = 0
    averageNearScore = []

    # Adds all same type knn scores together
    for key, value in output.items():
        counter = 0 # dict index
        for x in value:
            # Adds knn together based on classifer
            test = test + value[counter][0]
            counter = counter + 1
        # Average value based on n many items
        averageNearScore.append(test/len(value)/ len(value))

    # Gets lowest average score if there is a matching value it will return the first encountered item
    minnium = min(averageNearScore)

    # returns the classifer of the smallest average dict type
    return list(output.keys())[averageNearScore.index(minnium)]

# Lets make toast used for running findfriends mutiple times.
def ScreamingProcesser(iterations=None, kNear=None, startData=None, endData=None, classifer=None, printVal=None, split=None):
    iterationsReset = iterations    # used for reset iterations
    kNearReset = kNear + 1          #Formatting
    averageList = []                #Stores averages for each knn

    while kNear > 0:
        runningTotal = 0
        iterations = iterationsReset
        while iterations > 0:
            # 3  and 7 is what i want here -----------------------------------
            temp = Primer(kNear, startData, endData, classifer, split)
            runningTotal = runningTotal + temp
            iterations = iterations - 1

        averageList.append(round(runningTotal / iterationsReset, 2))
        if(printVal == True):
            print("|| Neighbors || ", kNear, " || Average Accuracy || " ,round(runningTotal / iterationsReset, 2), "%")
        kNear = kNear - 1

    if(printVal == True):
        # Plot stuff
        averageList = averageList[::-1]
        averageList = [0] + averageList
        plt.bar(range(kNearReset), averageList)
        plt.xticks(range(0, kNearReset))
        plt.title("K Nearest Neighbors")
        plt.xlabel("How Many Neighbors")
        plt.ylabel("Precents")
        plt.show()

    return averageList[1:len(averageList)]

def main():
    now = time.time()
    print("More iterations take longer")
    value =  int(input("Please enter iteration: \n    "))
    print("Loading... . ")
    print("_________________________________________________________")
    averageList = ScreamingProcesser(iterations=value, classifer=1, startData=3, endData=6, kNear=10, split=.6, printVal=True)
    print("_________________________________________________________")
    index = max(averageList)
    print("Most Accurate KNN")
    print("|| Neighbors || ", averageList.index(index), " || Average Accuracy || ", max(averageList), "%")
    print("_________________________________________________________")
    later = time.time()
    print("Complete ||    || Time elasped || ", round((later - now)/60, 2), " Minutes")


if __name__ == '__main__':
    main()
