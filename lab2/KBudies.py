import pandas as pd
from sklearn.utils import shuffle
from math import sqrt
import numpy as np
from matplotlib import pyplot as plt

#________________________________________________________________________________________
# Name: George Shea     ßeta
# Date Created: 6/10/21
# Date Modified 6/10/21
# Lab 2 find knn for give data
# Version 2.0
#________________________________________________________________________________________


path = pd.ExcelFile('C:/Users/gshea/Desktop/School/Summer2021/Artifical/DataSets/fruits_classification.xlsx')
dataFramePrime = pd.read_excel(path)                        #Allows for sheet reading


def Primer(k=None, dataStart=None, dataEnd=None):
    # Randomises the Data And Splits it into a 60/40 split
    df = shuffle(dataFramePrime)    #randomises data
    train = df.sample(frac=0.6)     #splits
    test = df.drop(train.index)     #splits

    #Find friends up the ladder
    average = FindFriends(train, test, k, dataStart, dataEnd)
    return average

def FindFriends(train, test, k=None, dataStart=None, dataEnd=None):
    # 1 goes through test data and does k nearest for each training data
    # 2 using knn makes a guess
    # 3 finnaly average correct guess verses total

    friends = []
    friendsIndex = []
    topFriends = []
    testCounter = 0
    matchCount = 0

    # Goes through each item in test
    for index, rowTest in test.iterrows():
        # Reset per indivual test
        topFriends = []
        friends = []
        friendsIndex = []
        trainCounter = 0
        # and then does k nearest to each item in train data.
        for index, rowTrain in train.iterrows():
            # K nearest neighbor 3, 6 default for fruits
            # start value is start of useable info and end is the final collum
            value = 0
            s = dataStart
            while s <= dataEnd:
                value = value + ((train.iloc[trainCounter::, s].values[0] - test.iloc[testCounter::, s].values[0])**2)
                s = s + 1

            # Adds neighbor and its index to the list
            friends.append(sqrt(value))
            friendsIndex.append((trainCounter))
            trainCounter = trainCounter + 1

        # f is the nearest neighbor, fI is its index in the train data set
        fI, f = np.array(friendsIndex), np.array(friends)
        # Sorts index list based on nearest
        inds = f.argsort()
        fI, f = fI[inds], f[inds]

        #Get x nearest neighbors ie top scores
        i = 0
        while i <= k:
            topFriends.append(train.iloc[fI[i], 1])
            i = i + 1

        # Runs most frequent and returns most frequent in case of tie returns first encountered.
        guess = MostFrequent(topFriends)
        if(test.iloc[testCounter, 1] == guess):
            matchCount = matchCount + 1

        testCounter = testCounter + 1
    # finnaly returns average
    return round(matchCount / len(test) * 100, 2)

def MostFrequent(listCount):
    # first encountered item in list will be returend in case of Apple, apple, Orange Orange. Apple would be returned
    mostCommon = max(listCount, key=listCount.count)
    return mostCommon


# Lets make toast used for running findfriends mutiple times.
def ScreamingProcesser(iterations, kNear):
    iterationsReset = iterations    # used for reset iterations
    kNearReset = kNear + 1          #Formatting
    averageList = []                #Stores averages for each knn

    while kNear > 0:
        runningTotal = 0
        iterations = iterationsReset
        while iterations > 0:
            temp = Primer(kNear, 3, 6)
            runningTotal = runningTotal + temp
            iterations = iterations - 1

        averageList.append(round(runningTotal / iterationsReset, 2))
        print("|| Neighbors || ", kNear, " || Average Accuracy || " ,round(runningTotal / iterationsReset, 2), "%")
        kNear = kNear - 1

    # Plot stuff
    averageList = averageList[::-1]
    averageList = [0] + averageList
    plt.bar(range(kNearReset), averageList)
    plt.xticks(range(0, kNearReset))
    plt.title("K Nearest Neighbors")
    plt.xlabel("How Many Neighbors")
    plt.ylabel("Precents")
    plt.show()

    return averageList
def main():
    print("More iterations take longer")
    value =  int(input("Please enter iteration: \n    "))
    print("Loading... . ")
    print("_________________________________________________________")
    averageList = ScreamingProcesser(value, 10)
    print("_________________________________________________________")
    index = max(averageList)
    print("Most Accurate KNN")
    print("|| Neighbors || ", averageList.index(index), " || Average Accuracy || ", max(averageList), "%")
    print("_________________________________________________________")
    print("Complete")
main()
