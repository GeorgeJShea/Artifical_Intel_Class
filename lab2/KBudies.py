import pandas as pd
from sklearn.utils import shuffle
from math import sqrt
import numpy as np
from matplotlib import pyplot as plt
import time
from collections import Counter

#________________________________________________________________________________________
# Name: George Shea     ßeta
# Date Created: 6/10/21
# Date Modified 8/10/21
# Lab 2 find knn for give data
# Version 2.21
#________________________________________________________________________________________



# put your path here
path = ('C:/Users/gshea/Desktop/School/Summer2021/Artifical/DataSets/fruits_classification.xlsx')

extentsion = path.split(".")[1]
if (extentsion == "xlsx"):
    path = pd.ExcelFile(path)
    dataFramePrime = pd.read_excel(path)
if (extentsion == "csv"):
    dataFramePrime = pd.read_csv(path)

def Primer(k=None, dataStart=None, dataEnd=None, classifer=None):
    endOf = dataFramePrime.iloc[:, dataStart:dataEnd+1]
    endOf = (endOf - endOf.mean()) / endOf.std()
    startOF = dataFramePrime.iloc[:, :dataStart]
    result = startOF.join(endOf)
    normalizedDf = shuffle(result)    #randomises data

    train = normalizedDf.sample(frac=0.6)     #splits best resutls apear to be closer to higher ratio of training data
    test = normalizedDf.drop(train.index)     #splits this is due to the algrothem being "lazy"

    #Find friends up the ladder
    average = FindFriends(train, test, k, dataStart, dataEnd, classifer)
    return average

def FindFriends(train, test, k=None, dataStart=None, dataEnd=None, classifer=None):
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
            # K nearest neighbor 3, 6 default for fruit
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
            topFriends.append(train.iloc[fI[i], classifer])
            i = i + 1

        # Runs most frequent and returns most frequent in case of tie returns first encountered.
        guess = MostFrequent(topFriends, f[:k])

        #------------------------ change to 2
        if(test.iloc[testCounter, classifer] == guess):
            matchCount = matchCount + 1

        testCounter = testCounter + 1
    # finnaly returns average
    return round(matchCount / len(test) * 100, 2)

def MostFrequent(listCount, fI):
    # creates tuple of knn score and item
    mergedList = [(fI[i], listCount[i]) for i in range(0, len(fI))]
    output = {}

    # Created dic and sorts by item
    for x, y in mergedList:
        if y in output:
            output[y].append((x, y))
        else:
            output[y] = [(x, y)]

    test = 0
    counter = 0
    averageNearScore = []
    # Adds all same type knn scores together
    for key, value in output.items():
        counter = 0
        for x in value:
            # addes knn scores together bases on same item
            test = test + value[counter][0]
            counter = counter + 1
        # averages knn scores from n items
        averageNearScore.append(test/len(value)/ len(value))

    # gets lowests average as that is the collests items
    # if there is a matching item somehow || it will take the istance of the first matching item from said set of matching items
    minnium = min(averageNearScore)
    # gets dic keys index into based on index of shortest item

    data = Counter(listCount)
    test = data.most_common(1)[0][0]

    return list(output.keys())[averageNearScore.index(minnium)]


# Lets make toast used for running findfriends mutiple times.
def ScreamingProcesser(iterations=None, kNear=None, startData=None, endData=None, classifer=None):
    iterationsReset = iterations    # used for reset iterations
    kNearReset = kNear + 1          #Formatting
    averageList = []                #Stores averages for each knn

    while kNear > 0:
        runningTotal = 0
        iterations = iterationsReset
        while iterations > 0:
            # 3  and 7 is what i want here -----------------------------------
            temp = Primer(kNear, startData, endData, classifer)
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
    now = time.time()
    print("More iterations take longer")
    value =  int(input("Please enter iteration: \n    "))
    print("Loading... . ")
    print("_________________________________________________________")
    averageList = ScreamingProcesser(iterations=value, classifer=1, startData=3, endData=6, kNear=10)
    print("_________________________________________________________")
    index = max(averageList)
    print("Most Accurate KNN")
    print("|| Neighbors || ", averageList.index(index), " || Average Accuracy || ", max(averageList), "%")
    print("_________________________________________________________")
    later = time.time()
    print("Complete ||    || Time elasped || ", round((later - now)/60, 2), " Minutes")
main()
